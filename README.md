# YaMDb API

The YaMDb API allows you to interact with the RESTful API of a fictional YaMDb review service for creative works like movies, books, and music.

## Features

1. Getting a list of all reviews for a title
2. Getting a review or comment by ID
3. Getting a list of comments to a review
4. CRUD for reviews and comments

## Installation

1. Fork and clone the repository
2. Set up a virtual environment
3. Install the dependencies: `pip install -r requirements.txt`

## Usage

### Authorization

To get access to the API, make a POST request with your **email address** to `/api/v1/auth/email`, after which you will receive a confirmation code. Next, submit a POST request to `/api/v1/auth/token` with your email address and the confirmation token. In response, you'll receive a JWT token. When calling the API, pass the token in the header as **Authorization: Bearer**.

### Example requests and responses

Sample POST request to `/api/v1/titles/{title_id}/reviews/`:

```
{
	"text": "Friends is the best sitcom ever!",
	"score": 10
}
```

Sample response:

```
{
	"id": 0,
	"text": "Friends is the best sitcom ever!",
	"author": "sergeyrodin",
	"score": 10,
	"pub_date": "2021-04-05T14:15:22Z"
}
```

Sample POST request to `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` to add a comment to the post above (id=3):

```
{
	"text": "I'd argue that HIMYM is better.",
}
```

Sample response:

```
{
	"id": 0,
	"text": "I'd argue that HIMYM is better.",
	"author": "andrewzhang",
	"pub_date": "2021-04-06T14:15:22Z"
}
```

See [the complete API specification (redoc.yaml)](https://github.com/RodinGolodin/api_yamdb_completed/blob/master/static/redoc.yaml).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
