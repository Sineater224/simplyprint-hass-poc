import logging
from datetime import timedelta
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)
DOMAIN = "simplyprint_custom"
API_URL = "https://api.simplyprint.io/95259/printers/Get"

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up SimplyPrint sensors from a config entry UI setup."""
    api_key = config_entry.data.get("api_key")
    session = async_get_clientsession(hass)

    async def async_update_data():
        """Fetch data from the SimplyPrint API."""
        try:
            async with async_timeout.timeout(10):
                headers = {"X-API-KEY": api_key}
                response = await session.get(API_URL, headers=headers)
                response.raise_for_status()
                data = await response.json()
                
                printer_dict = {}
                items = data.get("data", [])
                if isinstance(data, list):
                    items = data
                
                for item in items:
                    p_id = str(item.get("id"))
                    printer_info = item.get("printer", {})
                    job_info = item.get("job") or {}
                    notifications = item.get("notifications", [])
                    
                    combined = {**printer_info, **job_info}
                    combined["id"] = p_id
                    combined["notifications"] = notifications
                    printer_dict[p_id] = combined
                    
                return printer_dict
        except Exception as err:
            raise UpdateFailed(f"Error communicating with SimplyPrint API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="simplyprint_api",
        update_method=async_update_data,
        update_interval=timedelta(seconds=60),
    )

    await coordinator.async_refresh()

    entities = []
    if not coordinator.data:
        _LOGGER.error("SimplyPrint API returned no printers!")
        return
        
    for printer_id, p_data in coordinator.data.items():
        printer_name = p_data.get("name", f"Printer {printer_id}")
        
        entities.append(SimplyPrintStatusSensor(coordinator, printer_id, printer_name))
        entities.append(SimplyPrintProgressSensor(coordinator, printer_id, printer_name))
        entities.append(SimplyPrintHotendTempSensor(coordinator, printer_id, printer_name))
        entities.append(SimplyPrintBedTempSensor(coordinator, printer_id, printer_name))

    async_add_entities(entities)

# (BaseSensor, StatusSensor, ProgressSensor, HotendTempSensor, BedTempSensor 
# classes remain identical to the sticky/status-mapped version we built previously)