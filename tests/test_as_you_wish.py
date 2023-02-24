from asyouwish import Config

config = Config()
config.define("service.api_key", "YOUR_API_KEY_HERE", "required to connect to the API service")
config.define("service.oauth_token", "YOUR_API_OAUTH_TOKEN_HERE", "the oauth token used to login")
config.define("server.ipaddr", "127.0.0.1", "the ip address to host the server on")
config.define("server.port", 8080, "the port to choose for the server")
config.define("server.threads", 8, "the maximum number of threads to use for the web server")

config.define("server.colors.primary", (255, 160, 50), "the primary color of the user interface")
config.define("server.colors.secondary", (50, 255, 67), "the secondary color of the user interface")
print(config)

config.load("config.ini")

print("API_KEY:", config.get("service.api_key"))
print("API_AUTH_TOKEN:", config.get("service.oauth_token"))

hostname = config.get("server.ipaddr")
port = config.get("server.port")
thread_count = config.get("server.threads")
print(f"Starting server on {hostname}:{port} with {thread_count} threads.")

color1 = config.get("server.colors.primary")
print(f"Primary color: ({color1[0]}, {color1[1]}, {color1[2]})")