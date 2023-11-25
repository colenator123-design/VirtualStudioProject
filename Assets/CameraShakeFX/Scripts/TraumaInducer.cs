using UnityEngine;
using System.Collections;

/* Example script to apply trauma to the camera or any game object */
public class TraumaInducer : MonoBehaviour
{
    private void Start()
    {
    }

    /* Search for all the particle system in the game objects children */
    private void PlayParticles()
    {
        var children = transform.GetComponentsInChildren<ParticleSystem>();
        for (var i = 0; i < children.Length; ++i)
        {
            children[i].Play();
        }
        var current = GetComponent<ParticleSystem>();
        if (current != null) current.Play();
    }

    public void Explosion()
    {
        /* Play all the particle system this object has */
        PlayParticles();
    }
}