def recurrentErlangformula(capacity, trafficLoad):
  """
  Recurrent Erlang-B formula: B(0) = 1, B(c) = (A * B(c-1)) / (c + A * B(c-1)).

  """
  B = 1.0
  for c in range(1, capacity + 1):
    B = (trafficLoad * B) / (c + trafficLoad * B)
  return B
