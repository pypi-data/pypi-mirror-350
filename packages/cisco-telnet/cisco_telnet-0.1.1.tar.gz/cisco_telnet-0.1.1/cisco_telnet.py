import telnetlib3
import asyncio

async def apply_telnet_config(commands, host, username, password, enable_pass=None):
    try:
        reader, writer = await telnetlib3.open_connection(host)
        await reader.read_until("Username: ")
        writer.write(username + "\n")
        await reader.read_until("Password: ")
        writer.write(password + "\n")

        writer.write("enable\n")
        if enable_pass:
            await reader.read_until("Password: ")
            writer.write(enable_pass + "\n")

        writer.write("conf t\n")
        output = await reader.read_until("(config)#", timeout=2)
        print(output)

        for cmd in commands:
            writer.write(cmd + "\n")
            await asyncio.sleep(0.3)
            response = await reader.read_very_eager()
            print(f"==> {cmd}")
            print(response)

        writer.write("exit\n")
        print("\nНалаштування виконано успішно!")
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"\nПомилка під час виконання Telnet: {e}")