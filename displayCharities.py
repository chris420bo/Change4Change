def get_org_info(cur):
    try:
        cur.execute("SELECT name, description FROM Charity ORDER BY name ASC")
        res = cur.fetchall()
        print(res)
        names = []
        descriptions = []
        for org in res:
            names.append(org[0])
            descriptions.append(org[1])
        return names, descriptions
    except Exception as e:
        print('Error getting name and description: ', e)
        return None
