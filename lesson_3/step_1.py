from pprint import pprint

from pymongo import MongoClient

# создаем новую базу данных
client = MongoClient('127.0.0.1', 27017)
db = client['users1308']

# создаем коллекцию в новой бд
persons = db.persons

# # добовление одного документа в коллекцию
# persons.insert_one({
#     'name': 'Peter',
#     'age': 37,
#     'tags': ['cool', 'hot', 'ice']
# })

# # добовление нескольких документов в коллекцию
# persons.insert_many([{'name': 'Pete',
#                       'age': 39,
#                       'tags': ['hot']},
#                      {'name': 'Jhon',
#                       'age': 58,
#                       'tags': ['cool', 'ice']},
#                      {'name': 'Joan',
#                       'age': 43,
#                       'tags': ['cool']}
#                      ])

# # обновляем первый встреченый подходящий док в коллекции
# persons.update_one({'name': 'Pete'}, {'$set': {'age': 38}})
# # обновляем все подходящие доки в коллекции
# persons.update_many({'name': 'Pete'}, {'$set': {'age': 38}})

docs = [{'name': 'Pete2',
         'age': 47,
         'tags': ['cool2']},
        {'name': 'Pete3',
         'age': 46,
         'tags': ['cool3']},
        {'name': 'Pete6',
         'age': 46,
         'tags': ['cool6']}
        ]

for doc in docs:
    persons.update_one(
        {'name': doc['name']},
        {'$set': doc},
        upsert=True
    )
for doc in persons.find({}):
    pprint(doc)
#
# # обновляем первый встреченый подходящий док в коллекции из другого дока(структура исходного дока сохранится)
# persons.update_one({'name': 'Pete'}, {'$set': doc})

# # заменяем первый встреченый подходящий док в коллекции из другого дока(структура исходного дока сменится на новый)
# # persons.replace_one({'name': 'Pete'}, doc)

# # удаляем первый встреченый подходящий док в коллекции
# persons.delete_one({'name': 'Pete'})
# # удаляем все подходящие доки в коллекции
# # persons.delete_many({'name': 'Pete'})

# # считаем количество вхождений подходящего дока в коллекции(в данном примере все доки)
count = persons.count_documents({})
print(count)

# # варианты поиска и вывода данных
# for doc in persons.find({}):
#     pprint(doc)

# for doc in persons.find({'name': 'Pete', 'age': 39}):
#     pprint(doc)

# for doc in persons.find({'$or': [{'name': 'Pete'}, {'age': 58}]}):
#     pprint(doc)

# for doc in persons.find({'age': {'$lt': 39}}):
#     pprint(doc)

# for doc in persons.find({'age': {'$gt': 39}}):
#     pprint(doc)

# for doc in persons.find({'age': {'$gt': 39}}, {'name': 1, 'age': 1}):
# for doc in persons.find({'age': {'$gt': 39}}, {'name': 1, 'age': 1, '_id': 0}):
# for doc in persons.find({'age': {'$gt': 39}}, {'name': 1, 'age': 1, '_id': 0}).limit(2):
#     pprint(doc)

# pprint(list(persons.find({'age': {'$gt': 39}}))[-1])

# for doc in persons.find({}).sort('age'):
# for doc in persons.find({}).sort('age', -1):
#     pprint(doc)

# # удаляем коллекцию
# persons.drop()
