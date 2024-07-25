import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.List;

public class Main {
    public static List<byte[]> key_schedule(byte[] key, int rounds) throws NoSuchAlgorithmException {
        List<byte[]> schedule = new ArrayList<>();
        schedule.add(key);

        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        for (int i = 1; i < rounds; i++) {
            byte[] newKey = digest.digest(schedule.get(schedule.size() - 1));
            schedule.add(Arrays.copyOf(newKey, 16)); // 16바이트로 제한
        }
        return schedule;
    }

    public static byte[] inverse_feistel_network(byte[] block, byte[] roundKey) {
        byte[] left = Arrays.copyOfRange(block, 0, 8);
        byte[] right = Arrays.copyOfRange(block, 8, 16);
        byte[] f_result = new byte[8];
        for (int i = 0; i < 8; i++) {
            f_result[i] = (byte) (left[i] ^ roundKey[i]);
        }
        byte[] newLeft = new byte[8];
        for (int i = 0; i < 8; i++) {
            newLeft[i] = (byte) (right[i] ^ f_result[i]);
        }
        return concatenate(newLeft, left);
    }

    public static byte[] key_decrypt_alg(byte[] data, byte[] key, int rounds) throws NoSuchAlgorithmException {
        List<byte[]> keySched = key_schedule(key, rounds);
        byte[] decrypted = new byte[data.length];
        for (int i = 0; i < data.length; i += 16) {
            byte[] block = Arrays.copyOfRange(data, i, i + 16);
            for (int j = keySched.size() - 1; j >= 0; j--) {
                block = inverse_feistel_network(block, keySched.get(j));
            }
            System.arraycopy(block, 0, decrypted, i, 16);
        }
        return removePadding(decrypted);
    }

    private static byte[] concatenate(byte[] a, byte[] b) {
        byte[] result = new byte[a.length + b.length];
        System.arraycopy(a, 0, result, 0, a.length);
        System.arraycopy(b, 0, result, a.length, b.length);
        return result;
    }

    private static byte[] removePadding(byte[] data) {
        int i = data.length - 1;
        while (i >= 0 && data[i] == 0) {
            i--;
        }
        return Arrays.copyOf(data, i + 1);
    }

    public static byte[] key_decrypt(String key, String key2) throws NoSuchAlgorithmException {
        String base_key = key.concat("==");
        String base_key2 = key2.concat("=");

        byte[] deckey = Base64.getDecoder().decode(base_key);
        byte[] deckey2 = Base64.getDecoder().decode(base_key2);

        byte[] decrypted_key = key_decrypt_alg(deckey, deckey2, 16);

        return decrypted_key;
    }

    public static void exampleUsage() throws NoSuchAlgorithmException {
        //base64 encoded encrypted aes key's
        String key = "XH/vCWbu5we6dsge+MoN+w";
        //base64 encoded key of encrypted aes key(not for string encrypt)
        String key2 = "/zRuAnBg1NA";
        //base64 encoded original aes key
        String original_key = "Lnr4x+NC2k5dh28mgopMqA==";

        //decrypt aes key
        byte[] aes_key = key_decrypt(key, key2);

        //encode and compare with original key
        aes_key = Base64.getEncoder().encode(aes_key);
        System.out.println("original key =" + original_key);
        System.out.println("dectypted key =" + new String(aes_key));
    }

    public static void main(String[] args) throws NoSuchAlgorithmException {
        exampleUsage();
    }
}





