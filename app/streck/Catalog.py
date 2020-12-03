import pickle
import re
from collections import defaultdict

from playhouse.shortcuts import model_to_dict

from app.models.items import Items


class Catalog:

    @staticmethod
    def get_similiar_items(text):
        words = re.split("\s+", text.replace("\xa0", " ").lower())
        item_names = []
        main_name = None

        for w in words:
            item_names.append(w)
            if not main_name:
                main_name = w

        options = Items.select().where(Items.main_name.in_(item_names)).execute()
        options = [model_to_dict(i) for i in options]

        similar = []
        mean_params = [0]
        rmax = 0
        for i in options:
            score = len(set(i['name']) & set(item_names)) + (i['main_name'] in item_names) + (
                    i['main_name'] == main_name) * 3
            if score > 0:
                if i['params'] > 0:
                    mean_params.append(i['params'])

                similar.append({
                    "item": i,
                    "score": score,
                    "real_price": float(i['discount']) / i['params']
                })
                rmax = max(rmax, score)

        for s in similar:
            if s['item']['params'] < 0 < sum(mean_params):
                # params for this item not identified, but there are
                # items with params in options.
                s['item']['params'] = sum(mean_params) / len(mean_params) / 3
                s['real_price'] = float(s['item']['discount']) / s['item']['params']

        res = []
        for s in similar:
            if s['score'] == rmax:
                res.append(s)

        res = sorted(res, key=lambda s: s['real_price'])
        return res

    @staticmethod
    def get_items_by_shops(items):
        """
        items: list of all options
        return: dict of items in shops

        rebuild a list of items, that makes top 5 items in every shop
        """
        shops = defaultdict(list)

        for i in items:
            if len(shops[i['item']['shop']]) < 2:
                shops[i['item']['shop']].append({
                    "name": i['item']['name'],
                    "price": i['item']['discount'],
                    "img": i['item']['img'],
                    "real_price": i['real_price'],
                })

        return shops
