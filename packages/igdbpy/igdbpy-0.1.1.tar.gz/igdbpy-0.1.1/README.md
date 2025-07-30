# IgdbPy
A Python wrapper around the [Internet Game Database (IGDB)](https://www.igdb.com/) API

## Usage
```py
import igdbpy

key = igdbpy.generate_api_key(ID, SECRET)
wrapper = IgdbWrapper(ID, key)

data = wrapper.request_game(FIELD_QUERY)
more_data = wrapper.make_request(ENDPOINT, FIELD_QUERY)
```

## Authors
* [TonyGrif](https://github.com/TonyGrif) - Creator and Maintainer

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) for details
