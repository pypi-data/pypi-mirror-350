import sys
import kute.routines._calculate_transport_coefficient as calculate_transport_coefficient
import kute.routines._calculate_microscopic_current as calculate_microscopic_current
import kute.routines._join_currents as join_currents

routines = {"calculate_transport_coefficient": calculate_transport_coefficient, 
            "calculate_microscopic_current": calculate_microscopic_current,
            "join_currents": join_currents}

def main():
    STRING_AVAILABLE = f"Available routines: {list(routines.keys())}"
    if len(sys.argv) == 1:
        print(STRING_AVAILABLE)
        return
    if sys.argv[1] in routines:
        sys.argv[0] = "kute " + sys.argv[1]
        name = sys.argv.pop(1)
        routines[name].main()
    else:
        print(STRING_AVAILABLE)
        sys.exit(1)
        
if __name__ == "__main__":
    main()