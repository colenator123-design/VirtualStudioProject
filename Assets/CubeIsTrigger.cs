using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class CubeIsTrigger : MonoBehaviour
{
    public GameObject bomb;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }

    private void OnTriggerEnter(Collider other)
    {
        bomb.GetComponent<TraumaInducer>().Explosion();
    }
}
