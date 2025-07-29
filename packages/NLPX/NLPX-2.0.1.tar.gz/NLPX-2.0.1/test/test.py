import polars as pl

if __name__ == '__main__':
	s = pl.Series(["Brown", "Panda", "Polar"])
	print(isinstance(s.dtype, str))
	s1 = s.cast(str)
	# print(s1.dtype)
	s2 = s1.cast(pl.Categorical)
	# print(s2.dtype)
	s3 = s2.cat
	# print(s2)
	print(s3.get_categories().to_list())
	print(s3.to_local().to_physical().to_numpy())
