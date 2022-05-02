import pandas as pd
from datetime import datetime

class Problem(object):

    def read_data(self, filename):
        self.data = pd.read_csv(filename)
        return self.data
    
    def get_nearest_date_prev(self, items, current_date):
        return min(items, key=lambda x: abs(x - current_date))

    def get_no_of_days(self, current_date, nearest_date):
        delta = current_date - nearest_date
        return delta.days if delta.days <= 365 else 365

    def calculate_date(self, t_val, f_val, n):
        """
        Calculate Value = Tval - ((F_val-150)/365)*(365 - n)
        """
        return (t_val - ((f_val-150)/365)*(365 - n))

    def get_nearest_value_prev(self, items, nearest_date):
        value = 0
        for item in items:
            if item['date'] == nearest_date.strftime("%d/%m/%Y"):
                value = item['value']
                break
        return value

    def write_data(self):
        self.yDatesList = []
        self.yList = []
        self.finalList = []
        column = ['element', 'date', 'value', 'value_overlayed', 'final_value']
        data = []
        offsets = [None, *self.data.to_dict('recoreds'), None] # create list of offsets from given csv data.
        for prev, current, nxt in zip(offsets, offsets[1:], offsets[2:]):
            # get prev, current, nxt iteration from offsets
            if prev is not None: # check if previous is None
                if current['value_overlayed'] == 'N': # check if current value_overlayed is N
                    self.nearest_date = self.get_nearest_date_prev(self.yDatesList, datetime.strptime(current['date'], '%d/%m/%Y').date())
                    self.nearest_value = self.get_nearest_value_prev(self.yList, self.nearest_date)
                    self.no_of_days = self.get_no_of_days(datetime.strptime(current['date'], '%d/%m/%Y').date(), self.nearest_date)
                    self.final_value = self.calculate_date(current['value'], self.nearest_value, self.no_of_days)
                    current['final_value'] = round(self.final_value)
                    self.finalList.append(current)
                else:
                    self.yDatesList.append(datetime.strptime(current['date'], '%d/%m/%Y').date())
                    self.yList.append(current)
                    current['final_value'] = current['value']
                    self.finalList.append(current)
            else:
                current['final_value'] = current['value']
                self.finalList.append(current)

        #write data to csv file
        for value in self.finalList:
            data.append([v for v in value.values()])
        
        output = pd.DataFrame(data, columns=column)
        output.to_csv('output.csv')
        print("Output csv file is created successfully!")


if __name__ == '__main__':
    obj = Problem()
    obj.read_data('input.csv')
    obj.write_data()