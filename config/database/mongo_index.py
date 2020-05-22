
from config.database import mongo


class CreateIndex:

    @classmethod
    def good_category(cls):
        set = mongo['goodCategory']
        set.create_index([('sub_category_id', 1)])
        set.create_index([('sub_category_id', 1), ('fake_total_sales_number', -1)])
        set.create_index([('sub_category_id', 1), ('jumei_price', 1)])
        set.create_index([('sub_category_id', 1), ('jumei_price', -1)])
        set.create_index([('sub_category_id', 1), ('deal_comments_number', -1)])
        print(len(set.index_information()))


    @classmethod
    def good_static_detail(cls):
        set = mongo['goodStaticDetail']
        set.create_index([('store_id', 1)])
        print(set.index_information())

    @classmethod
    def good_dynamic_detail(cls):
        set = mongo['goodDynamicDetail']
        set.create_index([('item_id', 1)])
        print(set.index_information())

    @classmethod
    def good_comment(cls):
        set = mongo['goodComment']
        set.create_index([('product_id', 1)])
        set.create_index([('item_id', 1)])
        print(set.index_information())

    @classmethod
    def act_page(cls):
        set = mongo['goodComment']
        set.create_index([('act_page', 1)])
        print(set.index_information())

    @classmethod
    def merchant(cls):
        set = mongo['merchant']
        set.create_index([('store_id', 1)])
        print(set.index_information())

    @classmethod
    def act(cls):
        set = mongo['act']
        set.create_index([('url', 1)])
        print(set.index_information())

    @classmethod
    def category_filter(cls):
        set = mongo['categoryFilter']
        set.create_index([('category_id', 1)])
        print(set.index_information())

    @classmethod
    def cart(cls):
        set = mongo['cart']
        set.create_index([('phoneNum', 1)])
        print(set.index_information())

    @classmethod
    def information(cls):
        set = mongo['information']
        set.create_index([('id', 1)])
        set.create_index([('phoneNum', 1)])
        print(set.index_information())

print(CreateIndex)