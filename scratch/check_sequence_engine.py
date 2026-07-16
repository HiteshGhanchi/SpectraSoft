from core.sequence_engine import SequenceEngine

engine = SequenceEngine(uart=object())
print(engine._source_name_to_nibble)
print(engine.get_source_nibble('1: Normal Spark'))
print(engine.get_source_nibble('3: Combined Spark'))
print(engine.get_source_nibble('5: Cleaning Spark'))
