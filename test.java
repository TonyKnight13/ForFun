import java.util.*;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

public class test {
    public static void main(String[] args){
        String testS = "a,b,c,d";
        String[] prefixStrings = { "tc", "zj" };
        Map<String,String> testMap = new HashMap<String,String>();
        testMap.put("星期日", "Sunday");

        String jsonStr= JSON.toJSONString(testMap);
        ArrayList<String> tcEntityList = new ArrayList<>(Arrays.asList(testS.split(",")));
        ArrayList<String> zjEntityList = new ArrayList<>(Arrays.asList(testS.split(",")));
        ArrayList[] entityListofList = {tcEntityList, zjEntityList};
        for(int i = 0; i < 2;i++){
            for(int j = 0;j<entityListofList[i].size();j++){
                System.out.println(entityListofList[i].get(j));
            }
           
        }
    }
}