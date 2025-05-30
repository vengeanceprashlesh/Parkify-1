from vehicle import Vehicle
from parking_system import ParkingSystem

def test_parking_system_functionality():
    system = ParkingSystem(2)

    v1 = Vehicle("KA01AB1234")
    v2 = Vehicle("KA02CD5678")
    v3 = Vehicle("KA03EF9012")

    system.park_vehicle(v1)
    system.park_vehicle(v2)
    system.park_vehicle(v3)  # Should go to queue

    assert system.parking_lot.size() == 2
    assert system.waiting_queue.size() == 1

    system.remove_vehicle_recursive("KA01AB1234")  # Should allow KA03EF9012 to enter

    assert system.parking_lot.size() == 2
    assert system.waiting_queue.size() == 0

    system.remove_vehicle_recursive("NOTEXIST")  # Edge case

    print("✅ All test cases passed!")

if __name__ == '__main__':
    run_tests()
