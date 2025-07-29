from dotenv import load_dotenv
import os

load_dotenv()

# GPIO BCM codes
GPIO_PIN_VOPEN = int(os.getenv("GPIO_PIN_VOPEN", 2))
GPIO_PIN_VSTOP = int(os.getenv("GPIO_PIN_VSTOP", 3))
GPIO_PIN_VCLOSE = int(os.getenv("GPIO_PIN_VCLOSE", 4))

