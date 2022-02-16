class Red:
    data = {}

    @staticmethod
    def put(key, value):
        previous_list = Red.data.get(key, [])
        previous_list.append(value)
        Red.data[key] = previous_list


class BankOfReds:
    whichPV = {}
    consumers = {}
