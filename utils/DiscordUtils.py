import configs.DefaultConfig as defaultConfig

# Checks to see if the author ID is this ID
def is_me(ctx):
    return ctx.author.id == int(defaultConfig.discord_owner_id)
