package christmas;

import java.util.Arrays;
import java.util.List;

public enum EventEnumCategories {
    APPITIZER("애피타이저", Arrays.asList(EventEnumMenus.SOUP, EventEnumMenus.TAPAS, EventEnumMenus.SALAD)),
    MAIN("메인", Arrays.asList(EventEnumMenus.STAKE, EventEnumMenus.RIB, EventEnumMenus.SEAPASTA,
            EventEnumMenus.CHIRSTPASTA)),
    DESSERT("디저트", Arrays.asList(EventEnumMenus.CAKE, EventEnumMenus.ICECREAM)),
    DRINK("음료", Arrays.asList(EventEnumMenus.COKE, EventEnumMenus.WINE, EventEnumMenus.SHAMPAIGN));

    private String title;
    private List<EventEnumMenus> menus;

    EventEnumCategories(String title, List<EventEnumMenus> menus) {
        this.title = title;
        this.menus = menus;
    }

    public List<EventEnumMenus> getMenus() {
        return menus;
    }
}
