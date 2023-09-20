
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Linq;

public class HeadTracking : MonoBehaviour
{
    public UDPReceive uDPReceive;
    public GameObject cameraObject;
    List<Vector3> coords = new List<Vector3>();
    List<Vector3> rotaions = new List<Vector3>();
    Vector3 origin = new Vector3();
    Vector3 x_axis = new Vector3();
    Vector3 y_axis = new Vector3();
    Vector3 z_axis = new Vector3();
    
    public float x_ratio = 10;
    public float y_ratio = 10;
    public float z_ratio = 10;
    // Start is called before the first frame update
    void Start()
    {
        origin = cameraObject.transform.position;
        x_axis = cameraObject.transform.right;
        y_axis = cameraObject.transform.up;
        z_axis = cameraObject.transform.forward;
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
        // flip the y axis and z axis due to the diffs from openCV and unity
        float x = float.Parse(points[0]) - 0.5f;
        float y = 1f - (float.Parse(points[1]) - 0.5f);
        float z = 1f - (float.Parse(points[2]) - 0.5f);
        
        coords.Add(new Vector3(x * x_ratio, y * y_ratio, z * z_ratio));
        Vector3 avgCoord = AvgOfList(coords, 50);
        cameraObject.transform.position = origin + avgCoord.x * x_axis + avgCoord.y * y_axis + avgCoord.z * z_axis;

        rotaions.Add(new Vector3(float.Parse(points[3]) * Mathf.Rad2Deg,
            float.Parse(points[4]) * Mathf.Rad2Deg, float.Parse(points[5]) * Mathf.Rad2Deg));
        cameraObject.transform.rotation = Quaternion.Euler(AvgOfList(rotaions, 50));
    }

    Vector3 AvgOfList(List<Vector3> list, int limit)
    {
        while (list.Count > limit)
            list.RemoveAt(0);
        Vector3 sum = new Vector3();
        foreach (Vector3 vec in list)
            sum += vec;
        return sum / (float)limit;
    }
}