from core.database import get_session
from core.models import AnalyticalGroup, SourceCode

session = get_session()
try:
    groups = session.query(AnalyticalGroup).all()
    print('groups', len(groups))
    for g in groups[:5]:
        print('group', g.id, g.name)
        print('page_01_source=', g.page_01_source)
    rows = session.query(SourceCode).order_by(SourceCode.entry_no).all()
    print('source_codes=', [(r.entry_no, r.name) for r in rows])
finally:
    session.close()
