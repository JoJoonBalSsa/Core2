package christmas;

enum EventEnumMenus {
    SOUP("양송이수프", 6000),
    TAPAS("타파스", 5500),
    SALAD("시저샐러드", 8000),
    STAKE("티본스테이크", 55000),
    RIB("바비큐립", 54000),
    SEAPASTA("해산물파스타", 35000),
    CHIRSTPASTA("크리스마스파스타", 25000),
    CAKE("초코케이크", 15000),
    ICECREAM("아이스크림", 5000),
    COKE("제로콜라", 3000),
    WINE("레드와인", 60000),
    SHAMPAIGN("샴페인", 25000);

    private final String name;
    private final int price;

    EventEnumMenus(String name, int price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    public static EventEnumMenus containingEnum(String menu) {
        for (EventEnumMenus eventEnumMenus : EventEnumMenus.values()) {
            if (eventEnumMenus.getName().equals(menu)) {
                return eventEnumMenus;
            }
        }

        return null;
    }
}