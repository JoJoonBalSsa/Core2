import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.List;

public class Main {
    public static List<byte[]> alg2_key_schedule(byte[] key, int rounds) throws NoSuchAlgorithmException {
        List<byte[]> schedule = new ArrayList<>();
        schedule.add(key);

        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        for (int i = 1; i < rounds; i++) {
            byte[] newKey = digest.digest(schedule.get(schedule.size() - 1));
            schedule.add(Arrays.copyOf(newKey, 16)); // 16바이트로 제한
        }
        return schedule;
    }

    public static byte[] alg2_inverse_feistel_network(byte[] block, byte[] roundKey) {
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

    public static byte[] alg2_decrypt(byte[] data, byte[] key, int rounds) throws NoSuchAlgorithmException {
        List<byte[]> keySched = alg2_key_schedule(key, rounds);
        byte[] decrypted = new byte[data.length];
        for (int i = 0; i < data.length; i += 16) {
            byte[] block = Arrays.copyOfRange(data, i, i + 16);
            for (int j = keySched.size() - 1; j >= 0; j--) {
                block = alg2_inverse_feistel_network(block, keySched.get(j));
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
    public static void main(String[] args) throws NoSuchAlgorithmException {
        String key2 = "/rRXgwxk/Lk=";
        String key = "JfZkXxiIIxpXR0hJIuEgQw==";
        byte[] deckey = Base64.getDecoder().decode(key);
        byte[] deckey2 = Base64.getDecoder().decode(key2);

        byte[] asdf = alg2_decrypt(deckey, deckey2, 16);

        byte[] asdf2 = Base64.getEncoder().encode(asdf);
        System.out.println(new String(asdf2));
    }
}


