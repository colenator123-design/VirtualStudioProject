
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
    const float width = 480f;
    const float length = 640f;
    const float depth = 100f;

    public float max_x = 1, min_x = 1;
    public float max_y = 1, min_y = 1;
    public float max_z = 1, min_z = 1;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        string data = uDPReceive.data;
        if (data.Length < 1)
            return;
        data = data.Remove(0, 1);
        data = data.Remove(data.Length - 1, 1);
        string[] points = data.Split(',');

        print(points[0]);

        float x = (length - float.Parse(points[0])) / length;
        float y = (width - float.Parse(points[1])) / width;
        float z = (depth - float.Parse(points[2])) / depth;
        Debug.Log(z);
        xList.Add(min_x + x * (max_x - min_x));
        yList.Add(min_y + x * (max_y - min_y));
        zList.Add(min_z + x * (max_z - min_z));

        if (xList.Count > 50) { xList.RemoveAt(0); }
        if (yList.Count > 50) { yList.RemoveAt(0); }
        if (zList.Count > 50) { zList.RemoveAt(0); }

        float xAverage = Queryable.Average(xList.AsQueryable());
        float yAverage = Queryable.Average(yList.AsQueryable());
        float zAverage = Queryable.Average(zList.AsQueryable());

        cameraObject.transform.localPosition = new Vector3(xAverage, yAverage, zAverage);
    }
}