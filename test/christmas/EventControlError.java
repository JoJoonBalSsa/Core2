package christmas;
import java.util.Base64;
import javax.crypto.spec.SecretKeySpec;
import javax.crypto.SecretKey;
import javax.crypto.KeyGenerator;
import javax.crypto.Cipher;
import java.lang.reflect.Method;

import static java.lang.Integer.parseInt;

import java.util.ArrayList;

public class EventControlError {
private static final String ENCRYPTION_KEY_EVENTCONTROLERROR = "69SlW2T4Mud+r82l10Tllg==";

public static final String[] STRING_LITERALS_EVENTCONTROLERROR = {
"8zctVJfmNbRn8a9eBv2Ev5X1O+2qRi2KMNRcVgOmo6UcZeeN4atSjTvYCTkywsPsCE/rhVUqnR8nop8+clZRXmKxki6xQDIreQluxcljD+A=",
"8zctVJfmNbRn8a9eBv2Ev5X1O+2qRi2KMNRcVgOmo6UcZeeN4atSjTvYCTkywsPsCE/rhVUqnR8nop8+clZRXmKxki6xQDIreQluxcljD+A=",
"Zy2+yXUF6QqPuawBJzP2wO+xDpMyXctJThUN+Lnem/s/Ql5UCTZ5U/rQyKUUaWxdziRn8Dn+wu2Bp724tV8LQtxGg0DX4Kzjb0P+tWLHJfk=",
"Zy2+yXUF6QqPuawBJzP2wO+xDpMyXctJThUN+Lnem/s/Ql5UCTZ5U/rQyKUUaWxdziRn8Dn+wu2Bp724tV8LQtxGg0DX4Kzjb0P+tWLHJfk=",
"yuPlivU13pvPeE1x4P/7gQ==",
"pQ+zxJtBidEUGC0LWiSp4A==",
"Zy2+yXUF6QqPuawBJzP2wHrTX0uvOBRy9AdLdKM+RnMl7iV2PfrFM1xZW+LsE10ObWhRXsFYqWVe5+m8SwTySQ==",
"Zy2+yXUF6QqPuawBJzP2wHrTX0uvOBRy9AdLdKM+RnMl7iV2PfrFM1xZW+LsE10ObWhRXsFYqWVe5+m8SwTySQ==",
"8zctVJfmNbRn8a9eBv2Ev74JYqM4uMEh3ecKuFxZt+XEfhxU9duElFuRVk9P+dwRCE/rhVUqnR8nop8+clZRXmKxki6xQDIreQluxcljD+A=",
"zc8qg3DHASh9kFOBJtlQ1bKNweLjZjT/1nplNtJGU8X6VV83Ro2ReSVF9rbOZbFF8HDqzNIM6BlbyVyGonTiS5zIbjBddiO5/Fw7TlIz9Lo=",
"Zy2+yXUF6QqPuawBJzP2wDZIZD8k0Emhls05fUxgIEJVRypeY1IhGtuyvU0vOD2zziRn8Dn+wu2Bp724tV8LQtxGg0DX4Kzjb0P+tWLHJfk=",
"Zy2+yXUF6QqPuawBJzP2wDZIZD8k0Emhls05fUxgIEJVRypeY1IhGtuyvU0vOD2zziRn8Dn+wu2Bp724tV8LQtxGg0DX4Kzjb0P+tWLHJfk=",
"IxgZIbyRmV0WdrS/VdimzTZIZD8k0Emhls05fUxgIEJ2ZsukIct8wC/bgCogIcQC6YiN9s4BJii/7bC1JuKD7oMhK1f4ZGAA+larxo2pE2c=",
"IxgZIbyRmV0WdrS/VdimzTZIZD8k0Emhls05fUxgIEJ2ZsukIct8wC/bgCogIcQC6YiN9s4BJii/7bC1JuKD7oMhK1f4ZGAA+larxo2pE2c=",
"Zy2+yXUF6QqPuawBJzP2wB2OX4L91cKnHep/K9Alil08CuRW43HlYqplzCb0HTaEqF4ZH2MC3U1OA/LXaxLbzQ==",
"Zy2+yXUF6QqPuawBJzP2wB2OX4L91cKnHep/K9Alil08CuRW43HlYqplzCb0HTaEqF4ZH2MC3U1OA/LXaxLbzQ==",
"Zy2+yXUF6QqPuawBJzP2wBdhOTgTzxsNL1KggfLmZNQgZW8Xtr3tNmo3msz/Jn7I",
"Zy2+yXUF6QqPuawBJzP2wBdhOTgTzxsNL1KggfLmZNQgZW8Xtr3tNmo3msz/Jn7I",
"T/opwWUIILVpE6UC4Koe7YpRBOafZGU9eAzEnQ5vx+gQSrNU15L6LupwvJjXSpVl",
"T/opwWUIILVpE6UC4Koe7YpRBOafZGU9eAzEnQ5vx+gQSrNU15L6LupwvJjXSpVl"
};


        static{
		try {
			Class<?> decryptorClass = Class.forName("christmas.AES");
        Method decryptMethod = decryptorClass.getMethod("decrypt", String.class, String.class);
        for (int i = 0; i < STRING_LITERALS_EVENTCONTROLERROR.length; i++) {
        STRING_LITERALS_EVENTCONTROLERROR[i] = (String) decryptMethod.invoke(null, STRING_LITERALS_EVENTCONTROLERROR[i], ENCRYPTION_KEY_EVENTCONTROLERROR); 
        }
		} catch (Exception e) {
		}
		
        }
        
    public static void checkDateError(String date) {
        if (!date.chars().allMatch(Character::isDigit)) {
            System.out.println(STRING_LITERALS_EVENTCONTROLERROR[0]);
            throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[1]);
        } else if (parseInt(date) < 1 || parseInt(date) > 31) {
            System.out.println(STRING_LITERALS_EVENTCONTROLERROR[2]);
            throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[3]);
        }
    }

    public static void checkMenuError(String menu) {
        if (isOneMenu(menu)) {
            checkOneMenuErrors(menu);
            onlyDrinksError(EventModel.getOrderedMenu());
            return;
        }
        checkManyMenuErrors(menu);
    }

    private static boolean isOneMenu(String menu) {
        for (int i = 0; i < menu.length(); i++) {
            if (menu.charAt(i) == ',') {
                return false;
            }
        }
        return true;
    }

    private static void checkOneMenuErrors(String oneMenu) {
        checkMenuFormError(oneMenu);
        String[] menuInfo = oneMenu.split(STRING_LITERALS_EVENTCONTROLERROR[4]);
        checkMenuNameError(menuInfo[0]);
        checkMenuCountError(menuInfo[1]);
        checkMenuDuplicateError(menuInfo[0]);
        
        EventModel.setOrderedMenu(menuInfo);
    }

    private static void checkManyMenuErrors(String menu) {
        String[] menus = menu.split(STRING_LITERALS_EVENTCONTROLERROR[5]);
        for (String oneMenu : menus) {
            checkOneMenuErrors(oneMenu);
        }
        onlyDrinksError(EventModel.getOrderedMenu());
    }

    private static void checkMenuFormError(String menu) {
        for (int i = 0; i < menu.length(); i++) {
            if (menu.charAt(i) == '-') {
                return;
            }
        }
        System.out.println(STRING_LITERALS_EVENTCONTROLERROR[6]);
        throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[7]);
    }

    private static void checkMenuCountError(String menu) {
        if (!menu.chars().allMatch(Character::isDigit)) {
            System.out.println(STRING_LITERALS_EVENTCONTROLERROR[8]);
            throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[9]);
        } else if (parseInt(menu) < 1) {
            System.out.println(STRING_LITERALS_EVENTCONTROLERROR[10]);
            throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[11]);
        } else if (parseInt(menu) > EventModel.getLeftMenus()) {
            System.out.println(STRING_LITERALS_EVENTCONTROLERROR[12]);
            throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[13]);
        }
    }

    private static void checkMenuNameError(String menu) {
        if (EventEnumMenus.containingEnum(menu) == null) {
            System.out.println(STRING_LITERALS_EVENTCONTROLERROR[14]);
            throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[15]);
        }
    }

    private static void checkMenuDuplicateError(String menu) {
        for (String[] orderedMenu : EventModel.getOrderedMenu()) {
            if (orderedMenu[0].equals(menu)) {
                System.out.println(STRING_LITERALS_EVENTCONTROLERROR[16]);
                throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[17]);
            }
        }
    }

    private static void onlyDrinksError(ArrayList<String[]> menus) {
        if (isOnlyDrinks(menus)) {
            System.out.println(STRING_LITERALS_EVENTCONTROLERROR[18]);
            throw new IllegalArgumentException(STRING_LITERALS_EVENTCONTROLERROR[19]);
        }
    }

    private static boolean isOnlyDrinks(ArrayList<String[]> menus) {
        EventEnumCategories category = EventEnumCategories.DRINK;
        for (String[] menu : menus) {
            EventEnumMenus tempName = EventEnumMenus.containingEnum(menu[0]);
            if (!category.getMenus().contains(tempName)) {
                return false;
            }
        }
        return true;
    }
}



class AES {

    public static String decrypt(String encryptedText, String key) {
        try {
        byte[] keyBytes = Base64.getDecoder().decode(key);
        SecretKeySpec secretKey = new SecretKeySpec(keyBytes, "AES");

        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(encryptedText));
        return new String(decryptedBytes, "UTF-8");
        } catch (Exception e) {
            throw new RuntimeException("Decryption failed", e);
    }
    }
}

