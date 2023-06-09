
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;
 
public class HeadTracking : MonoBehaviour
{
    public UDPReceive uDPReceive;
    public GameObject cameraObject;
    List<float> xList = new List<float>();
    List<float> yList = new List<float>();
    List<float> zList = new List<float>();
 
 
    // Start is called before the first frame update
    void Start()
    {
        
    }
 
    // Update is called once per frame
    void Update()
    {
        string data = uDPReceive.data;
        if(data.Length < 1)
            return;
        data = data.Remove(0, 1);
        data = data.Remove(data.Length-1, 1);
        string[] points = data.Split(',');
 
        print(points[0]);
 
        float x = (float.Parse(points[0])-320) / 100;
        float y = (float.Parse(points[1])-240) / 100;
        float z = (float.Parse(points[2]) ) / 30 ;
        Debug.Log(z);
        xList.Add(x);
        yList.Add(y);
        zList.Add(z);
 
        if (xList.Count > 50) { xList.RemoveAt(0); }
        if (yList.Count > 50) { yList.RemoveAt(0); }
        if (zList.Count > 50) { zList.RemoveAt(0); }
 
        float xAverage = Queryable.Average(xList.AsQueryable());
        float yAverage = Queryable.Average(yList.AsQueryable());
        float zAverage = Queryable.Average(zList.AsQueryable());
 
 
        Vector3 cameraPos = cameraObject.transform.localPosition;
        // Vector3 cameraRot = cameraObject.transform.localPosition;
 
 
        cameraObject.transform.localPosition = new Vector3(-23f - xAverage, 1.3f- yAverage, 11 + zAverage);
        // cameraObject.transform.localEulerAngles = new Vector3(18.76f- yAverage * 10, xAverage * 10 , 0);
 
    }
}