
"""
Author: Jai Prakashsingh
Email: jvoltci@gmail.com
"""

import random
import json
import boto3

class ParkingLot:
    def __init__(self, square_footage, spot=96):
        self.spots = [""] * (square_footage // spot)

    def is_full(self):
        return "" not in self.spots

    def map_vehicles(self):
        vehicle_map = {}
        for i, spot in enumerate(self.spots):
            if spot != "":
                vehicle_map[i] = spot
        return vehicle_map

class Car:
    def __init__(self, plate):
        self.plate = plate

    def __str__(self):
        return self.plate

    def park(self, parking_lot):
        while True:
            spot = random.randint(0, len(parking_lot.spots) - 1)
            if parking_lot.spots[spot] == "":
                parking_lot.spots[spot] = self.plate
                print(f'Car with license plate {self} parked successfully in spot {spot}')
                break
            else:
                print(f'Car with license plate {self} was not parked successfully in spot {spot}. Trying again...')


def main():    

    parking_lot = ParkingLot(2000)
    cars = [Car('UP651301'), Car('UP6513374'), Car('UP651341')]
    while cars and not parking_lot.is_full():
        car = cars.pop()
        car.park(parking_lot)


    vehicle_map = parking_lot.map_vehicles()
    with open('vehicle_map.json', 'w') as f:
        json.dump(vehicle_map, f)

    # Set up AWS credentials
    session = boto3.Session(
        aws_access_key_id='YOUR_ACCESS_KEY_ID',
        aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
    )
    s3 = session.resource('s3')

    # upload file to S3 bucket
    s3.meta.client.upload_file('vehicle_map.json', 'my-bucket', 'vehicle_map.json')


if __name__ == '__main__':
    main()

