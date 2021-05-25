from flask import Flask, request, redirect, url_for, abort, Response

from utils import check_privilege, redirect_sessionless
from discount import brands, users, generate_discount_codes

import random

app = Flask(__name__)

@app.route('/')
def index_page():
	return '''
Welcome! If you are a brand and would like to check discount check:
<ul>
<li><a href="/generate">Page for generating discount codes.</a></li>
<li><a href="/list">Page for viewing discount codes.</a></li>
</ul>
If you're a user, check <a href="/fetch">this page</a> to see available discount codes.
'''


def validate_brand_id(brand_id):
	if brand_id not in brands:
		abort(Response("Please provide a brand. (?brandId=Billogram).", status=400))


def validate_user_id(user_id):
	if user_id not in users:
		abort(Response("Please provide a user. (?userId=Technomunk)", status=400))


# Brand frontend

@app.route('/list')
def list_codes_page():
	# Mock user validation
	redirect_sessionless(url_for('.index_page'))
	check_privilege('enum_discount')

	# brand would be in the session for any brand-admin user
	brand_id = request.args.get('brandId')
	validate_brand_id(brand_id)
	return { 'brand': brand_id, 'discountCodes': brands[brand_id], }


@app.route('/generate', methods=['GET', 'POST'])
def generate_code_page():
	redirect_sessionless(url_for('.index_page'))
	check_privilege('create_discount')
	
	if request.method == 'POST':
		# Generate discount codes
		# NOTE: brand id may be part of the session in a "real" app
		brand_id = request.form.get('brandId')
		validate_brand_id(brand_id)
		count = request.form.get('count', type=int)
		if count < 1:
			abort(Response("Count must be a natural number.", status=400))

		generate_discount_codes(brand_id, count)
		return redirect(url_for('.list_codes_page', brandId=brand_id))
	else:
		# Present discount code generation form
		# brand would be in the session for any brand-admin user
		brand_id = request.args.get('brandId')
		validate_brand_id(brand_id)
		return f'''<form method="post">
<label for="count">Count:</label>
<input id="count" name="count" type="number" min="1">
<input type="hidden" name="brandId" value="{brand_id}">
<input type="submit" value="Submit">
</form>'''


# User frontend

@app.route('/fetch')
def fetch_code_page():
	redirect_sessionless(url_for('.index_page'))

	# NOTE: user_id should be in the session object in a "real" app
	user_id = request.args.get('userId')
	validate_user_id(user_id)

	user_brands = users[user_id]
	response = '<ul>'
	for brand in brands:
		if brand in user_brands:
			response += f'<li>{brand}: {user_brands[brand]}</li>'
		else:
			# check that a brand has available discount codes
			if brands[brand]:
				response += f'''<li><form action="{url_for('.share_info_page')}" method="post">
{brand}: <input type="submit" value="Share info">
<input type="hidden" name="brandId" value="{brand}">
<input type="hidden" name="userId" value="{user_id}">
</form></li>'''
			else:
				response += f'<li>{brand}: no discount codes available.</li>'
	response += '</ul>'
	return response


@app.route('/share_info', methods=['POST'])
def share_info_page():
	user_id = request.form.get('userId')
	validate_user_id(user_id)
	brand_id = request.form.get('brandId')
	validate_brand_id(brand_id)
	discount_codes = brands[brand_id]
	if not discount_codes:
		abort(Response("No discount codes found for provided brand.", status=406))
	users[user_id][brand_id] = random.choice(discount_codes)
	return redirect(url_for('.fetch_code_page', userId=user_id))
