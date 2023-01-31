import pandas as pd


def to_db(users):
    topics = ["Link", "Name", "Manipulative commenting", "Link to authority", "Hyperbolize", "Artificial contrast", "Call to action", "Stuff", "Islam", "Drugs", "Politic", "Christianity", "Extremism", "Suicide", "Words count"]
    db = pd.DataFrame(columns=topics)
    users = users[0]
    db["Link"] = [item[7] for item in users]
    db["Name"] = [item[6] for item in users]
    db["Manipulative commenting"] = [item[0] for item in users]
    db["Link to authority"] = [item[1] for item in users]
    db["Hyperbolize"] = [item[2] for item in users]
    db["Artificial contrast"] = [item[3] for item in users]
    db["Call to action"] = [item[5] for item in users]
    db['Stuff'] = [item[4][1]*100/item[4][0] for item in users]
    db['Islam'] = [item[4][2]*100/item[4][0] for item in users]
    db['Drugs'] = [item[4][3]*100/item[4][0] for item in users]
    db['Politic'] = [item[4][4]*100/item[4][0] for item in users]
    db['Christianity'] = [item[4][5]*100/item[4][0] for item in users]
    db['Extremism'] = [item[4][6]*100/item[4][0] for item in users]
    db['Suicide'] = [item[4][7]*100/item[4][0] for item in users]
    db["Words count"] = [item[4][0] for item in users]
    db.to_excel('PsychoReader.xlsx')
