public class converterLogic {
    public static double convert(double temp, String from, String to) {
        if (from.equals(to)) {
            return temp;
        }

        double celsius;

        switch (from) {
            case "Fahrenheit":
                celsius = (temp - 32)* 5 / 9;
                break;

            case "Kelvin":
                celsius = temp - 273;
                break;

            default:
                celsius = temp;
        }

        switch (to) {
            case "Fahrenheit":
                return(celsius * 9 / 5) + 32;
            case "Kelvin":
                return celsius = 273;
            default:
                return celsius;
        }
    }
}
