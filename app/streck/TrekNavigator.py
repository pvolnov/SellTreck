from typing import List, Tuple

from playhouse.shortcuts import model_to_dict

from app.data_models import Item
from app.streck import Catalog
from app.models.shops import Shops


class TrekNavigator:

    def __init__(self):
        pass

    @staticmethod
    def calculate_total_price(cart: List[dict], shops: List[str]) -> Tuple[List[dict], int]:
        from collections import defaultdict

        final_cart = defaultdict(list)
        total = 0
        for i, item in enumerate(cart):

            mpr = 1e9
            shop_name = None

            for shop in shops:
                if shop in item:
                    if item[shop][0]['real_price'] <= mpr:
                        mpr = item[shop][0]['real_price']
                        shop_name = shop

            if shop_name is None:
                raise Exception("Not all products are available in these stores")

            final_cart[shop_name].append(i)
            total += item[shop_name][0]['price']

        result = [{"name": k,
                   "localcart": final_cart[k]} for k in final_cart]
        return result, total

    @staticmethod
    def get_nearest_shop(shop_name, latitude, longitude):
        shops = Shops.select().where(Shops.name == shop_name).order_by(
            (Shops.latitude - latitude) * (Shops.longitude - longitude)
            * (Shops.latitude - latitude) * (Shops.longitude - longitude)).limit(1).execute()

        return model_to_dict(shops[0])

    @staticmethod
    def get_yandex_url(points: List[Tuple[float, float]]) -> str:
        mean_latitude = sum([p[0] for p in points])
        mean_longitude = sum([p[0] for p in points])
        url = f"https://yandex.ru/maps/2/saint-petersburg/?ll={mean_latitude}%2C{mean_longitude}&mode=" \
              f"routes&rtext={points[0][0]}%2C{points[0][1]}"

        for point in points[1:]:
            url += f"~{point[0]}%2C{point[1]}"
        url += "&z=14"
        return url

    @staticmethod
    def get_fasted_trek(points: List[Tuple[float, float]]) -> Tuple[List[Tuple[float, float]], float]:
        import itertools
        best_trek = []
        mlen = 1e9
        for trek in list(itertools.permutations(points[1:-1])):
            length = 0
            ftrek = [points[0], *trek, points[-1]]
            for i in range(1, len(ftrek)):
                length += ((ftrek[i - 1][0] - ftrek[i][0]) ** 2 + (
                        ftrek[i - 1][1] - ftrek[i][1]) ** 2) ** 0.5 * 111 * 1.2
            if length < mlen:
                mlen = length
                best_trek = ftrek

        return best_trek, (mlen / 5) * 60 + (len(points) - 1) * 5

    @staticmethod
    def generate_options(length):
        options = []

        def add(prefix, min, max, n) -> list:
            if min + n > max:
                return
            if 0 == n:
                options.append(prefix)
                return

            prefix2 = [min] + prefix
            add(prefix, min + 1, max, n)
            add(prefix2, min + 1, max, n - 1)

        for n in range(1, length + 1):
            add([], 0, length, n)

        return options

    def generate_traks_for_cart(self, current_geo: Tuple[float, float], cart_list: List[Item]):
        cart = []
        shops_names = []  # all the possible shops
        for i in cart_list:
            items = Catalog.get_items_by_shops(Catalog.get_similiar_items(i['name']))
            cart.append(items)
            shops_names += list(items.keys())

        shops_names = list(set(shops_names))
        shops_geo = {}
        for s in shops_names:
            shop = self.get_nearest_shop(s, current_geo[0], current_geo[1])
            shops_geo[s] = (shop['latitude'], shop['longitude'])

        trek_options_ids = self.generate_options(len(shops_names))
        print("Find options:", len(trek_options_ids))
        trek_options_params = []

        for option in trek_options_ids:
            shops_trek = [shops_names[shop_id] for shop_id in option]

            geo_points = []
            for shop_name in shops_trek:
                geo_points.append(shops_geo[shop_name])

            # try:
            try:
                cart_by_stores, price = self.calculate_total_price(cart, shops_trek)
            except:
                continue
            fasted_trek, duration = self.get_fasted_trek([current_geo, *geo_points, current_geo])

            trek_options_params.append({
                "keypoints": fasted_trek,
                "duration": duration,
                "cart_by_stores": cart_by_stores,
                "price": price,
                "yandex_url": self.get_yandex_url(fasted_trek)
            })
            # except Exception as e:
            #     print(e)
            #     # trek not available
            #     pass

        return trek_options_params

    def genarete_treks_for_cart_list(self, current_geo, cart_list):
        treks = self.generate_traks_for_cart(current_geo, cart_list)
        minprice = min([t['price'] for t in treks])
        minduraturation = min([t['duration'] for t in treks])

        mind = minp = 1e9
        best_price_trek = best_duration_trek = None

        for idd, t in enumerate(treks):
            t['torsion'] = t['duration'] * 3.125 + t['price']
            t['id'] = idd

            if t['price'] == minprice:
                if t['duration'] < mind:
                    mind = t['duration']
                    best_price_trek = idd

            if t['duration'] == minduraturation:
                if t['price'] < minp:
                    minp = t['price']
                    best_duration_trek = idd

        sorted_treks = sorted(treks, key=lambda t: t['torsion'])
        res = list(set([t['id'] for t in sorted_treks[:3]] + [best_price_trek, best_duration_trek]))
        result = []
        for r in res:
            result.append(treks[r])
        return result
