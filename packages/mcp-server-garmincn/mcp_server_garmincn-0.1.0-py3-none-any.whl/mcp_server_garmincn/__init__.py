from mcp_server_garmincn.tools.garmin_health import garmin_service,mcp


def main():
    # init garmincn service, login
    if not garmin_service.init_api():
        print("Garmin API initialization failed")
        exit(1)
    print("Garmin API initialized successfully")

    mcp.run()

if __name__ == "__main__":
    main()

