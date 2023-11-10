using UnityEngine;

public class ObjectMovement : MonoBehaviour
{
    public Vector3[] points = new Vector3[4];
    public float speed = 30f;
    public float rotate_speed = 5f;

    private int currentTargetIndex = 0;
    public bool isRotate = false;

    private void Start()
    {
        points[0] = new Vector3(-164.88f, 19f, 411.69f);
        points[1] = new Vector3(-232.23f, 19f, 448.14f);
        points[2] = new Vector3(-193.89f, 19f, 519.81f);
        points[3] = new Vector3(-130.4f, 19f, 486.3f);
        // 开始时物体在A点
        transform.position = points[0];
        transform.forward = points[1] - points[0];
    }

    private void Update()
    {
        if (isRotate)
            Rotation();
        else
            MoveToNextPoint();
    }

    private void MoveToNextPoint()
    {
        Vector3 targetPoint = points[currentTargetIndex];
        // 使用Lerp平滑移动物体到目标位置
        // transform.position = Vector3.Lerp(transform.position, targetPoint, speed * Time.deltaTime);
        // transform.forward = points[currentTargetIndex] - transform.position;
        // transform.forward = transform.forward.normalized;
        transform.position += transform.forward * speed * Time.fixedDeltaTime;
    }
    private void Rotation()
    {
        Vector3 newForward = points[currentTargetIndex] - points[(currentTargetIndex + 3) % points.Length];
        newForward = newForward.normalized;
        transform.forward = Vector3.Lerp(transform.forward, newForward, rotate_speed * Time.fixedDeltaTime);
        // rotate till close enough
        if (Vector3.Distance(transform.forward, newForward) < 0.1f)
        {
            // transform.forward = newForward;
            transform.forward = points[currentTargetIndex] - transform.position;
            transform.forward = transform.forward.normalized;
            isRotate = false;
        }
    }
    private void OnTriggerEnter(Collider other)
    {
        // 移动到下一个点
        currentTargetIndex = (currentTargetIndex + 1) % points.Length;
        isRotate = true;
    }
}
