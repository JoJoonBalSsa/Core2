package christmas;

import static java.lang.Integer.parseInt;

import java.util.Scanner;


public class EventControl {
    EventControl() {
        EventView.firstScreen();
        inputDate();
        inputMenu();
        controlOrderedPrice();
        controlShampaignEvent();
        controlDiscounts();
        EventView.printFinalFee();
        controlBadge();
    }

    public void inputDate() {
        Scanner scan = new Scanner(System.in);
    	String date = scan.nextLine();
        while (catchDateError(date)) {
            EventView.tryAgainMessage();
            date = scan.nextLine();
        }

        EventModel.setDate(parseInt(date));
    }

    private boolean catchDateError(String date) {
        try {
            EventControlError.checkDateError(date);
            return false;
        } catch (IllegalArgumentException e) {
            return true;
        }
    }

    public void inputMenu() {
        EventView.orgerGuideMessage();

        Scanner scan = new Scanner(System.in);
    	String menu = scan.nextLine();
        while (catchMenuError(menu)) {
            EventModel.eraseOrderedMenu();
            EventView.tryAgainMessage();
            menu = scan.nextLine();
        }

        EventView.printOrderedMenu();
    }

    private boolean catchMenuError(String menu) {
        try {
            EventControlError.checkMenuError(menu);
            return false;
        } catch (IllegalArgumentException e) {
            return true;
        }
    }

    public void controlOrderedPrice() {
        EventModel.calculateOrderPrice(EventModel.getOrderedMenu());
        EventView.printOrderPrice();
    }

    public void controlShampaignEvent() {
        boolean isShampaignTrue = EventModel.isShampaignEvent(EventModel.getOrderPrice());
        EventView.printShampaignEvent(isShampaignTrue);
    }

    public void controlDiscounts() {
        new EventCalculateDiscounts();
        EventView.printDiscounts(EventModel.getDiscounts());
        EventView.printTotalDiscounts();
    }

    public void controlBadge() {
        String badge = EventEnumBadges.whichBadge(EventModel.getDiscounts());
        EventView.printBadge(badge);
    }
}
