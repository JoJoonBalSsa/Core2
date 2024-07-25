package christmas;
import java.lang.reflect.Method;

import java.text.DecimalFormat;

public class EventView {
private static final String ENCRYPTION_KEY_EVENTVIEW = "69SlW2T4Mud+r82l10Tllg==";

public static final String[] STRING_LITERALS_EVENTVIEW = {
"dUL9ICCFXh0SAppY5H2CAqXcN2BPU4Q/AkUmu6CMt6QNnik5f5+SVByK6RI4GW5SpMFRrWqUoiKTWG2JfVkU5OhUeokUzv5Wl4ZHLcZt4ZE=",
"e08LeStTDTsnlMcjec4owW7h9SY/cFWH5TrKalnm4/7W8HWf2M7JJbSZDcD6LikK73JCJOIE4+qssZ9lvkfASw2+b237NoFFFxGTwIbFrM9rUC+jjiKDZJ0oAekIGXaU",
"rugDz69Oi331kTeeYKoRtbt80SpqOy+ktcfIrqQOw7s=",
"TgsSQ46sgJz9wgY3RDIsJXBap1hvqmB3RZz0/OlXxjWVqL7blaj7/znEThXhwAEXTOQgtHPy0nYn25HHmPdboMuVP89/9FvErxeyJ3dPwDtpfAhlZpedT2YbFKhZ1E+WcOKx3Gs1MyX9ApW/4VreBlgMiueppmfyRS5as11fr/M=",
"BHOjtcnIuXEu2ZNEnmG0RQ==",
"+sKqrrlTunabezHyYWugWtxDa3KvAqQQWU7/zuqRKITKbJoWtanqTTBu1flbVvVtY7MQV4PxoiW8qPwJ90PBBwejsplus0AxKXVwFe5VScE=",
"0CfLDOR0MPOmmQSdB+xSV+9AOUiQzzciyJv/1bCIyUk=",
"yyPjMEqQswNujJ76debnnQ==",
"G5C3Ww+UdCK1YjYYCpBkJg==",
"h+fIJtjIrUJ57nyANIM2POijBunRRZ91Ek13KCqhWRHvQDlIkM83Isib/9WwiMlJ",
"JETwVrwTtx8aDW5JtnmFxA==",
"OdVG7BHtVLpCOSEL/C/NFQ==",
"oNsRwBzSN69jxrzAuIfeHCM8D7RN5nKke5l6B3H26eU=",
"TxMU/MqSv+0dcIlRx3w2A+qBmZXpCQRxKUnKRm3JHc4=",
"9FXdgTYPBDn6z4/UzNtyhg==",
"HNKkPcfyMimePXArr5nAyLJKFNdshkwZLB2iGUxEc3o=",
"9FXdgTYPBDn6z4/UzNtyhg==",
"JETwVrwTtx8aDW5JtnmFxA==",
"w1qq/uPBuKK5nkPnyMDK+/I6jC1bL2uzCtIFTF1uD2+l+zSD7QZDyN/ORkKqnrD8",
"OdVG7BHtVLpCOSEL/C/NFQ==",
"JETwVrwTtx8aDW5JtnmFxA==",
"tVvLKmN3tLzsQit1O7YeUsMDrA1KW00cf/SRJMy8Nx4=",
"OdVG7BHtVLpCOSEL/C/NFQ==",
"mWx2IYtWpWQTkVbznpUmccMDrA1KW00cf/SRJMy8Nx4=",
"OdVG7BHtVLpCOSEL/C/NFQ==",
"JETwVrwTtx8aDW5JtnmFxA==",
"B1MeszCYhhCMnMZvb86Er8MDrA1KW00cf/SRJMy8Nx4=",
"OdVG7BHtVLpCOSEL/C/NFQ==",
"JETwVrwTtx8aDW5JtnmFxA==",
"YF9NnfqBWb5loLU8uzYZe6X7NIPtBkPI385GQqqesPw=",
"OdVG7BHtVLpCOSEL/C/NFQ==",
"CHmcuKgV75xH5YKUVlwcQjUDlgibFw3/4gbmiuzJuYE=",
"JETwVrwTtx8aDW5JtnmFxA==",
"yuPlivU13pvPeE1x4P/7gQ==",
"OdVG7BHtVLpCOSEL/C/NFQ==",
"4amN2PbRQqVc0SxI7DiMSrMIJymWcyLzPGv2ECyO/VqpxsbJAAArX/QKAk/JQt4Z",
"JETwVrwTtx8aDW5JtnmFxA==",
"OdVG7BHtVLpCOSEL/C/NFQ==",
"Ch+QG3F35EiFYrzBM4zIhQyQalwUk/vH1MFsmR9K/XA="
};


        static{
		try {
			Class<?> decryptorClass = Class.forName("christmas.AES");
        Method decryptMethod = decryptorClass.getMethod("decrypt", String.class, String.class);
        for (int i = 0; i < STRING_LITERALS_EVENTVIEW.length; i++) {
        STRING_LITERALS_EVENTVIEW[i] = (String) decryptMethod.invoke(null, STRING_LITERALS_EVENTVIEW[i], ENCRYPTION_KEY_EVENTVIEW); 
        }
		} catch (Exception e) {
		}
		
        }
        
    public static void firstScreen() {
        System.out.println(STRING_LITERALS_EVENTVIEW[0]);
        System.out.println(STRING_LITERALS_EVENTVIEW[1]);
    }

    public static void tryAgainMessage() {
        System.out.println(STRING_LITERALS_EVENTVIEW[2]);
    }

    public static void orgerGuideMessage() {
        System.out.println(STRING_LITERALS_EVENTVIEW[3]);
    }

    public static void printOrderedMenu() {
        System.out.println(STRING_LITERALS_EVENTVIEW[5] + EventModel.getDate() + STRING_LITERALS_EVENTVIEW[4]);
        System.out.println(STRING_LITERALS_EVENTVIEW[6]);
        for (String[] menu : EventModel.getOrderedMenu()) {
            System.out.println(menu[0] + STRING_LITERALS_EVENTVIEW[8] + menu[1] + STRING_LITERALS_EVENTVIEW[7]);
        }
    }

    public static void printOrderPrice() {
        System.out.println(STRING_LITERALS_EVENTVIEW[9]);

        DecimalFormat df = new DecimalFormat(STRING_LITERALS_EVENTVIEW[10]);
        String money = df.format(EventModel.getOrderPrice());
        System.out.println(money + STRING_LITERALS_EVENTVIEW[11]);
    }

    public static void printShampaignEvent(boolean isShampaignEvent) {
        System.out.println(STRING_LITERALS_EVENTVIEW[12]);
        if (isShampaignEvent) {
            System.out.println(STRING_LITERALS_EVENTVIEW[13]);
            return;
        }
        System.out.println(STRING_LITERALS_EVENTVIEW[14]);
    }

    public static void printDiscounts(int discounts) {
        System.out.println(STRING_LITERALS_EVENTVIEW[15]);

        if (discounts != 0) {
            printChristmasDiscounts();
            printWeekdaysDiscounts();
            printSpecialDiscounts();
            printGoodsDiscounts();
            return;
        }
        System.out.println(STRING_LITERALS_EVENTVIEW[16]);
    }

    private static void printChristmasDiscounts() {
        if (EventModel.getChristmasDiscount() != 0) {
            DecimalFormat df = new DecimalFormat(STRING_LITERALS_EVENTVIEW[17]);
            String money = df.format(EventModel.getChristmasDiscount());
            System.out.println(STRING_LITERALS_EVENTVIEW[19] + money + STRING_LITERALS_EVENTVIEW[18]);
        }
    }

    private static void printWeekdaysDiscounts() {
        if (EventModel.getWeekDaysDiscount() != 0) {
            DecimalFormat df = new DecimalFormat(STRING_LITERALS_EVENTVIEW[20]);
            String money = df.format(EventModel.getWeekDaysDiscount());
            if (EventModel.getIsWeekEnds()) {
                System.out.println(STRING_LITERALS_EVENTVIEW[22] + money + STRING_LITERALS_EVENTVIEW[21]);
                return;
            }
            System.out.println(STRING_LITERALS_EVENTVIEW[24] + money + STRING_LITERALS_EVENTVIEW[23]);
        }
    }

    private static void printSpecialDiscounts() {
        if (EventModel.getSpecialDiscount() != 0) {
            DecimalFormat df = new DecimalFormat(STRING_LITERALS_EVENTVIEW[25]);
            String money = df.format(EventModel.getSpecialDiscount());
            System.out.println(STRING_LITERALS_EVENTVIEW[27] + money + STRING_LITERALS_EVENTVIEW[26]);
        }
    }

    private static void printGoodsDiscounts() {
        if (EventModel.getGoodsDiscount() != 0) {
            DecimalFormat df = new DecimalFormat(STRING_LITERALS_EVENTVIEW[28]);
            String money = df.format(EventModel.getGoodsDiscount());
            System.out.println(STRING_LITERALS_EVENTVIEW[30] + money + STRING_LITERALS_EVENTVIEW[29]);
        }
    }

    public static void printTotalDiscounts() {
        System.out.println(STRING_LITERALS_EVENTVIEW[31]);
        DecimalFormat df = new DecimalFormat(STRING_LITERALS_EVENTVIEW[32]);
        String money = df.format(EventModel.getDiscounts());
        if (EventModel.getDiscounts() != 0) {
            System.out.print(STRING_LITERALS_EVENTVIEW[33]);
        }
        System.out.println(money + STRING_LITERALS_EVENTVIEW[34]);
    }

    public static void printFinalFee() {
        System.out.println(STRING_LITERALS_EVENTVIEW[35]);
        DecimalFormat df = new DecimalFormat(STRING_LITERALS_EVENTVIEW[36]);
        String money = df.format(
                EventModel.getOrderPrice() - EventModel.getDiscounts() + EventModel.getGoodsDiscount());
        System.out.println(money + STRING_LITERALS_EVENTVIEW[37]);
    }

    public static void printBadge(String badge) {
        System.out.println(STRING_LITERALS_EVENTVIEW[38]);
        System.out.println(badge);
    }
}
