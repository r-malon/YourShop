from peewee import *
from datetime import datetime

db = SqliteDatabase('data.db', pragmas={
	'journal_mode': 'wal',
	'cache_size': -1024 * 32,
	'foreign_keys': 0,
	'ignore_check_constraints': 0
})

class BaseModel(Model):
	class Meta:
		database = db


class Item(BaseModel):
	desc = TextField()
	qty = IntegerField()
	price = FloatField()
	added_at = DateTimeField(default=datetime.utcnow)
