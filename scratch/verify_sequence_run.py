import os
os.environ['PYTHONPATH'] = '.'
from core.database import get_session
from core.models import AnalyticalGroup
from core.sequence_engine import SequenceEngine

class FakeUART:
    def __init__(self):
        self.commands = []
    def send_command(self, cmd, wait_ack=True):
        self.commands.append(cmd)
        return True
    def read_adc_value(self):
        return 123

class CountingSequenceEngine(SequenceEngine):
    def __init__(self, uart):
        super().__init__(uart)
        self.prespark_calls = []
    def execute_prespark(self, source_name, preburn_ms):
        self.prespark_calls.append((source_name, preburn_ms))
        print('PRESPARK', source_name, preburn_ms)
        return True
    def execute_integration(self, integ_ms, elements):
        print('INTEGRATION', integ_ms, len(elements))
        return {'mock': 1}
    def execute_clean(self, clean_ms):
        print('CLEAN', clean_ms)
        return True
    def execute_shutdown(self):
        print('SHUTDOWN')
        return True

session = get_session()
try:
    group = session.get(AnalyticalGroup, 1)
    page1 = group.page_01_source if group else {}
    print('DB page1:', page1)
    engine = CountingSequenceEngine(FakeUART())
    engine.execute_full_sequence(page1, [
        {'seq': '1', 'itg': 1, 'ele': 'Fe'},
        {'seq': '2', 'itg': 2, 'ele': 'Ni'},
        {'seq': '3', 'itg': 3, 'ele': 'Mn'},
    ])
    print('prespark calls:', engine.prespark_calls)
finally:
    session.close()
