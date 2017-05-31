# First order reversal curve (FORC) diagrams simulation

The FORC diagrams analysis is implemented by the FORC processors, for instance, by the PikeFORC class.
FORC analysis can be applied to a Magnetic matter simulating object which implements. 
For example, in order to simulate a single particle model use an instance of the SingleParticleMatter class, whose constructor takes in turn a MagneticParticle object.

```python
h = Hysteron(2.0, -2.0)
matter = SingleParticleMatter(h)
forc = PikeFORC(3, -1, 1, matter, output_directory)
forc.magnetization_forc()
forc.calculate_forc_distribution()
forc.draw_forc_diagram_hc_hu()
```

## Stoner-Wohlfarth model simulation

```python
p = SwParticle(np.pi/3)
p.draw(output_directory)
```

## References
1. [C.R. Pike, A.R. Roberts, K.L. Verosub, JAP **85** (1999), 6660-6666](http://dx.doi.org/10.1063/1.370176)
2. [M.V. Vaganov, J. Linke, S. Odenbach, Yu.L. Raikher, JMMM **431** (2015), 130-133](http://www.sciencedirect.com/science/article/pii/S0304885316319552)
3. [A.M. Biller, O.V. Stolbov, Yu.L. Raikher, Phys. Rev. E **92** (2015), 023202](https://doi.org/10.1103/PhysRevE.92.023202)
