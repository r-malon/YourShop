from settings import *
from models import *
# app.config.from_envvar('YOURAPPLICATION_SETTINGS')

@app.before_first_request
def first_run():
	try:
		db.create_tables([Item])
	except Exception as e:
		app.logger.error(e)
		db.close()

@app.before_request
def before_run():
	try:
		db.connect()
	except Exception as e:
		app.logger.error(e)
		db.close()

@app.teardown_request
def teardown(error=None):
	db.close()
	if error:
		app.logger.error(error)


@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html')

@app.route('/about')
@app.route('/sobre')
def about():
	return render_template('about.html')

@app.route('/add')
@app.route('/adicionar')
def add_item_page():
	return render_template('add.html')



@app.route('/items')
def list_items():
	search = request.args.get('search')
	order = request.args.get('order')
	start = request.args.get('start')
	limit = request.args.get('limit')

	query = Item.select()

	if search:
		query = query.where(Item.desc.contains(search))
	if order:
		order = order.split(',')
		columns = []
		if 'date' in order or 'added_at' in order:
			columns.append(Item.added_at.desc())
		if 'desc' in order:
			columns.append(Item.desc.desc())
		if 'qty' in order:
			columns.append(Item.qty.desc())
		if 'price' in order:
			columns.append(Item.price.desc())
		query = query.order_by(*columns)
	if start:
		query = query.offset(start)
	if limit:
		query = query.limit(limit)
	return jsonify(list(query.dicts()))


@app.route('/items', methods=['POST'])
def add_item():
	desc = request.form['desc']
	qty = request.form['qty']
	price = request.form['price']

	try:
		item = Item.create(
			desc=desc, 
			qty=qty, 
			price=price
		)

		if 'photo' in request.files:
			for file in request.files.getlist('photo'):
				if file and allowed_file(file.filename):
					filename = os.path.join(
						app.config['UPLOAD_FOLDER'], 
						secure_filename(f'{item.id}.{get_ext(file.filename)}')
					)
					file.save(filename)
		res = make_response(jsonify(
			{'message': 'Inserido com sucesso!', 'category': 'success'}), 201)
#		flash('Inserido com sucesso!', 'success')
	except Exception as e:
		res = make_response(jsonify(
			{'message': f'Erro: {e}', 'category': 'danger'}), 200)
#		flash(f'Erro: {e}', 'danger')
	finally:
		return '', 204
	'''
	response = make_response(json.dumps(data))
	response.status_code = 200
	response.headers['Access-Control-Allow-Origin'] = '*'
	'''

@app.route('/items/<int:item_id>', methods=['DELETE'])
def del_item(item_id):
	try:
		item = Item.get_by_id(item_id)
		item.delete_instance()
		res = make_response(jsonify(
			{'message': 'Deletado com sucesso!', 'category': 'success'}), 200)
	except Exception as e:
		res = make_response(jsonify(
			{'message': f'Erro: {e}', 'category': 'danger'}), 200)
	finally:
		return res


@app.errorhandler(404)
def not_found(e):
	return render_template('404.html'), 404



if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, threaded=True) #debug=True, ssl_context='adhoc')
