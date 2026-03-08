"""Supply Chain Agent for medical inventory management."""
from services.mcp_server import mcp_server
from typing import Dict, Any, List


class SupplyChainAgent:
    """Agent responsible for monitoring medical inventory and supplies."""
    
    def __init__(self):
        """Initialize the Supply Chain Agent."""
        self.role = "Medical Supply Chain Manager"
    
    def check_inventory_status(self, required_items: List[str] = None) -> Dict[str, Any]:
        """Check inventory status and generate alerts for low stock."""
        inventory_data = mcp_server.get_inventory_data()
        
        if not inventory_data:
            return {"status": "error", "message": "Unable to retrieve inventory data"}
        
        low_stock_items = []
        adequate_stock_items = []
        alerts = []
        
        for item_data in inventory_data:
            item = item_data['item']
            stock = item_data['stock']
            threshold = item_data['threshold']
            
            if required_items and item not in required_items:
                continue
            
            if stock <= threshold:
                low_stock_items.append({
                    "item": item,
                    "current_stock": stock,
                    "threshold": threshold,
                    "urgency": "high" if stock < threshold * 0.5 else "medium"
                })
                alerts.append(f"LOW STOCK: {item} - {stock} units (threshold: {threshold})")
            else:
                adequate_stock_items.append({"item": item, "current_stock": stock})
        
        return {
            "status": "critical" if len(low_stock_items) > 0 else "adequate",
            "low_stock_items": low_stock_items,
            "adequate_stock_items": adequate_stock_items,
            "alerts": alerts,
            "total_items_checked": len(inventory_data),
            "items_needing_reorder": len(low_stock_items)
        }


supply_chain_agent = SupplyChainAgent()
