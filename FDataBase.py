import psycopg2.extras
import time
import math
import re
from flask import Flask, url_for, flash


class FDataBase:
    def __init__(self, conn):
        self.__db = conn
        self.__cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def AddProduct(self, product_name, characteristic, cost, categories):
        try:
            self.__cur.execute("SELECT * FROM product WHERE product_name = %s ",
                               (product_name,))
            res = self.__cur.fetchone()
            if res:
                flash("A product with that name already exists")
                return False
            else:
                tm = math.floor(time.time())
                self.__cur.execute("INSERT INTO product (product_name, characteristic, cost, categories)"
                                   " VALUES (%s,%s,%s,%s)",
                                   (product_name, characteristic, cost, categories))
                self.__cur.execute("INSERT INTO product_categories (categories_product)"
                                   " VALUES (%s)",
                                   (categories,))
                return True
        except psycopg2.Error as e:
            print("Error getting article from database" + str(e))

    # def AddBasket(self, id_product):
    #     try:
    #         self.__cur.execute("SELECT * FROM product WHERE id = %s ",
    #                            (id_product,))
    #         res = self.__cur.fetchone()
    #         if res:
    #             flash("A product with that name already exists")
    #             return False
    #         else:
    #             tm = math.floor(time.time())
    #             self.__cur.execute("INSERT INTO users (user_basket)"
    #                                " VALUES (%s)",
    #                                (id_product))
    #             return True
    #     except psycopg2.Error as e:
    #         print("Error getting article from database" + str(e))

    def dellProduct(self, product_name):
        try:
            print("LIKE")
            self.__cur.execute('SELECT product_name, categories FROM product WHERE product_name = %s', (product_name,))
            res = self.__cur.fetchone()
            if res:
                delete_script = 'DELETE FROM product  WHERE product_name = %s'
                self.__cur.execute(delete_script, (product_name,))
                flash(f'Product "{product_name}" deleted!')
                return True
            else:
                flash(f'Error deleting: article "{product_name}" absent!')
                return False
        except psycopg2.Error as e:

            print("Error getting article from database 1" + str(e))
            return (f"The product with this name: {product_name} does not exist")

    def getPost(self, alias):
        try:
            self.__cur.execute('SELECT product_name, characteristic, cost '
                               'FROM product WHERE product_name LIKE %s', (alias,))
            res = self.__cur.fetchone()
            if res:
                return res
        except psycopg2.Error as e:
            print("Error getting article from database " + str(e))
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute("SELECT id, product_name, characteristic, cost FROM product")
            res = self.__cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Error getting article from database " + str(e))

        return []

    def getCategoriesAnonce(self):
        try:
            self.__cur.execute("SELECT categories_product FROM product_categories")
            res = self.__cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print("Error getting article from database " + str(e))

        return []

    def getCategories(self, categories):
        try:

            self.__cur.execute('SELECT categories_product, description_product '
                               'FROM product_categories WHERE categories_product LIKE %s', (categories,))

            res = self.__cur.fetchone()
            if res:
                return res
        except psycopg2.Error as e:
            print("Error getting article from database " + str(e))
        return (False, False)

    def getCategoriesSelect(self, categories):
        try:
            print(categories)
            self.__cur.execute('SELECT id, product_name, characteristic, cost FROM product '
                               ' WHERE categories LIKE %s', (categories,))
            res = self.__cur.fetchall()

            if res:
                return res
        except psycopg2.Error as e:
            print("Error getting article from database " + str(e))

        return []

    def addUser(self, email, psw, first_name, last_name, old, phone):
        try:
            self.__cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            res = self.__cur.fetchone()
            if res:
                flash("User with this email already exists")
                return False
            else:
                self.__cur.execute("INSERT INTO users (email, psw, first_name, last_name, old, phone) "
                                   "VALUES (%s,%s,%s,%s,%s,%s)",
                                   (email, psw, first_name, last_name, old, phone))
                flash(f"Registration is complete! Congratulations! {first_name}")
                return True
        except psycopg2.Error as e:
            print("Error getting article from database" + str(e))
            return False

    def getUser(self, id_user):
        try:
            self.__cur.execute("SELECT * FROM users WHERE id = %s", (id_user,))
            res = self.__cur.fetchone()
            if not res:
                print(f"User  {id_user} not found!")
                return False
            return res
        except psycopg2.Error as e:
            print("Error getting article from database" + str(e))
        return False

    def getUserByEmail(self, email, ):
        try:
            self.__cur.execute("SELECT * FROM users WHERE email  LIKE %s",
                               (email,))
            res = self.__cur.fetchone()
            if not res:
                flash(f"User  {email} not found!")
                return False

            return res
        except psycopg2.Error as e:
            print("Error getting article from database" + str(e))
        return False

    def create_post(self, title, author, pages_num, review):
        try:
            self.__cur.execute("INSERT INTO books (title, author, pages_num, review)"
                               "VALUES (%s, %s, %s, %s)",
                               (title, author, pages_num, review))
            flash(f'Статтю "{title}" додано  ')
        except psycopg2.Error as e:
            print("Error getting article from database" + str(e))

    def get_prof(self, id_user):
        self.__cur.execute("SELECT * FROM users WHERE id = %s ", (id_user))
        res = self.__cur.fetchone()
        print(res)
        if res:
            flash("Faind!")
            return res
        else:
            flash("ERROR!")
            return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
        try:
            binary = psycopg2.Binary(avatar)
            self.__cur.execute("UPDATE users SET avatar = %s WHERE id = %s", (binary, user_id,))
            self.__db.commit()
        except psycopg2.Error as e:
            print("Error getting article from database " + str(e))
            return False
        return True
