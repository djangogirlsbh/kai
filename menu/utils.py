# Update the session with the numbers of items in the basket
def update_count(session):
    count = 0
    for k, v in session.get('basket', {}).items():
        count += v

    session['count'] = count
