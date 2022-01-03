import numpy as np
def health_check(inventory):
    results=[]; total_value=0; excess_value=0; obsolete_value=0
    for item in inventory:
        value=item["qty"]*item["unit_cost"]
        total_value+=value
        daily_usage=item.get("daily_demand",0)
        dos=item["qty"]/max(daily_usage,0.01)
        turns=daily_usage*365/max(item["qty"],1)
        age_days=item.get("age_days",0)
        shelf_life=item.get("shelf_life_days",9999)
        health="healthy"
        if dos>180 or turns<2: health="excess"; excess_value+=value*max(0,(dos-90)/dos)
        if age_days>shelf_life*0.8: health="near_expiry"
        if daily_usage==0 and age_days>365: health="obsolete"; obsolete_value+=value
        if turns>=12: health="fast_mover"
        results.append({"sku":item["sku"],"value":round(value,0),"dos":round(dos,0),
                        "turns":round(turns,1),"health":health})
    return {"items":results,"total_value":round(total_value,0),"excess_value":round(excess_value,0),
            "obsolete_value":round(obsolete_value,0),"excess_pct":round(excess_value/max(total_value,1)*100,1)}
if __name__=="__main__":
    inv=[{"sku":"A","qty":500,"unit_cost":10,"daily_demand":5,"age_days":30},
         {"sku":"B","qty":50,"unit_cost":100,"daily_demand":2,"age_days":200},
         {"sku":"C","qty":1000,"unit_cost":5,"daily_demand":0,"age_days":400},
         {"sku":"D","qty":200,"unit_cost":20,"daily_demand":15,"age_days":10}]
    r=health_check(inv)
    print(f"Total: ${r['total_value']:,} | Excess: ${r['excess_value']:,} ({r['excess_pct']}%)")
    for i in r["items"]: print(f"  {i['sku']}: {i['health']} (turns={i['turns']}, DOS={i['dos']})")
