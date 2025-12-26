def recurrentErlangformula(capacity, trafficLoad):
  if (capacity == 0):
    return 1.0

  return (
    (trafficLoad * recurrentErlangformula(capacity - 1, trafficLoad)) /
    (capacity + trafficLoad * recurrentErlangformula(capacity - 1, trafficLoad))
  )

