package christmas;

import static java.lang.Integer.parseInt;

import java.util.ArrayList;

public class EventModel {
    private static int date;
    private static ArrayList<String[]> orderedMenu = new ArrayList<>();
    private static int leftMenus = 20;
    private static int orderPrice = 0;
    private static int christmasDiscount = 1000;
    private static int weekDaysDiscount = 0;
    private static int specialDiscount = 0;
    private static int goodsDiscount = 0;
    private static boolean isWeekEnds = false;
    private static int discounts = 0;

    public static void setOrderedMenu(String[] menuInfo) {
        orderedMenu.add(menuInfo);
        leftMenus -= parseInt(menuInfo[1]);
    }


    public static int getLeftMenus() {
        return leftMenus;
    }

    public static void setDate(int num) {
        date = num;
    }

    public static int getDate() {
        return date;
    }

    public static void setOrderPrice(int num) {
        orderPrice = num;
    }

    public static int getOrderPrice() {
        return orderPrice;
    }

    public static void setChristmasDiscount(int num) {
        christmasDiscount = num;
    }

    public static int getChristmasDiscount() {
        return christmasDiscount;
    }

    public static void setWeekDaysDiscount(int num) {
        weekDaysDiscount = num;
    }

    public static int getWeekDaysDiscount() {
        return weekDaysDiscount;
    }

    public static void setIsWeekEnds(boolean bool) {
        isWeekEnds = bool;
    }

    public static void setSpecialDiscount(int num) {
        specialDiscount = num;
    }

    public static int getSpecialDiscount() {
        return specialDiscount;
    }


    public static int getGoodsDiscount() {
        return goodsDiscount;
    }

    public static boolean getIsWeekEnds() {
        return isWeekEnds;
    }

    public static void setDiscounts(int num) {
        discounts = num;
    }

    public static int getDiscounts() {
        return discounts;
    }

    public static void eraseOrderedMenu() {
        orderedMenu.clear();
        leftMenus = 20;
    }

    public static ArrayList<String[]> getOrderedMenu() {
        return orderedMenu;
    }

    public static boolean isShampaignEvent(int orderPrice) {
        if (orderPrice >= 120000) {
            EventView.printShampaignEvent(true);
            goodsDiscount = 25000;
            return true;
        }
        return false;
    }

    public static void calculateOrderPrice(ArrayList<String[]> menus) {
        for (String[] menu : menus) {
            orderPrice += EventEnumMenus.containingEnum(menu[0]).getPrice() * parseInt(menu[1]);
        }
    }
}
