import random, string

brands = {
	"TechnoInc": [],
	"Billogram": [],
}

users = {
	"Technomunk": {},
}

def generate_discount_codes(brand, count=1):
	'''
	Generate new discount codes associated with provided brand.
	'''
	def generate_code():
		return ''.join(random.choice(string.ascii_letters) for _ in range(8))
	generated = [generate_code() for _ in range(count)]
	brands.setdefault(brand, []).extend(generated)
	return generated
