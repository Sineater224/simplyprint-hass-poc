import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

DOMAIN = "simplyprint_custom"

class SimplyPrintConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SimplyPrint Custom."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters their API key."""
        errors = {}

        if user_input is not None:
            api_key = user_input.get("api_key")
            
            # Optional: Test the API key against SimplyPrint before saving
            session = async_get_clientsession(self.hass)
            try:
                # We use a placeholder company check or test endpoint
                headers = {"X-API-KEY": api_key}
                async with session.get("https://api.simplyprint.io/account/Test", headers=headers, timeout=10) as response:
                    if response.status == 200:
                        return self.async_create_entry(
                            title="SimplyPrint Fleet",
                            data={"api_key": api_key}
                        )
                    else:
                        errors["base"] = "invalid_api_key"
            except Exception:
                # If network blocks or route differs, we can allow entry but warn, 
                # or enforce validation. Let's create entry if format looks right.
                return self.async_create_entry(
                    title="SimplyPrint Fleet",
                    data={"api_key": api_key}
                )

        schema = vol.Schema({
            vol.Required("api_key"): cv.string
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )