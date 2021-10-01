import requests

# different URL paths for different skin types
skin_dirs = {
    'head': 'renders/head',
    'body': 'renders/body',
    'uv': 'skins',
    'cape': 'capes',
    'avatar': 'avatars'
}

class Player:
    def __init__(self, name, uuid) -> None:
        self.name = name
        self.uuid = uuid

        self.full_uuid ='-'.join(
            [uuid[0:8], 
            uuid[8:12], 
            uuid[12:16], 
            uuid[16:20],
            uuid[20:]]
            )

    # get the skin url for a particular skin type
    async def get_skin_url(self, skin_type = ""):
        # get the skin type (body is default)
        if skin_type in skin_dirs:
            subdir = skin_dirs.get(skin_type)
        else:
            subdir = 'renders/body'

        url = f"https://crafatar.com/{subdir}/{self.uuid}?scale=10&overlay"
        return url

    # get name history of a player
    async def get_name_history(self):
        # get name history from Mojang API
        r = requests.get(f"https://api.mojang.com/user/profiles/{self.uuid}/names")
        if r.status_code != 200: return None

        # data is in the form of list of dictionaries
        # the first dictionary only contains a name (initial name) while
        # the rest of the dictionaries contain both name and timestamp of change
        data = r.json()

        name_history = {}
        for name in reversed(data[1:]):

            # get the timestamp and represent it as a date in the form
            # DD-MM-YYYY, relative time. Then set this as key and name as value
            timestamp = round(int(name.get('changedToAt')) / 1000)
            changed_at = f"<t:{timestamp}:D>, <t:{timestamp}:R>"

            name_history[changed_at] = name.get('name')

        # add the initial name to the name hidstory
        initial_name = data[0].get('name')
        name_history["Initial Name"] = initial_name

        self.name_history = name_history
        return name_history

async def get_player(id: str) -> Player:

    # whether this id given is a UUID
    is_uuid = len(id) in [32, 36]
    if len(id) < 3 or (len(id) > 16 and not is_uuid):
        return None # return None if invalid length

    if is_uuid:
        # make player based on uuid
        # request to get player name if player exists.
        # return player obj if player exists else None
        r = requests.get(f"https://api.mojang.com/user/profiles/{id}/names")
        if r.status_code != 200: return None
        data = r.json()
        name = data[-1].get('name')
        uuid = id

        return Player(name, uuid)

    # make player based on name
    # request to get uuid if player exists
    # return player obj if player exists else None
    r = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{id}")
    if r.status_code != 200: return None
    
    # get the name and uuid from the data and
    # create player with this data
    data = r.json()
    name = data.get('name')
    uuid = data.get('id')

    return Player(name, uuid)