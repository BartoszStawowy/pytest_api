


class UrlCreator:
    BASE_URL = 'https://restful-booker.herokuapp.com'

    def booking(self):
        booking_url = f'{self.BASE_URL}/booking'
        return booking_url
