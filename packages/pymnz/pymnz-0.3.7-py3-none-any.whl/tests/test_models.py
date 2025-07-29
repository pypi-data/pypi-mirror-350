from pymnz.models import Script


# Teste de execução
def test_models_script():
  def soma(a, b):
    print(f'A soma de {a} + {b} é {a + b}.')
    assert a + b == 3, "Problema no main"
    raise Exception('test')

  try:
    script = Script('Script de teste', soma, a=1, b=2)
    script.run(False)
  except Exception as e:
    assert str(e) == 'test'


# Teste de execução
def test_model_script_set_code_start():
  def soma(a, b):
    print(f'A soma de {a} + {b} é {a + b}.')
    assert a + b == 3, "Problema no main"
    return a + b
    
  def soma_start(a, b):
    print(f'A soma de {a} + {b} é {a + b}.')
    assert a + b == 4, "Problema no main"
    raise Exception('test')

  try:
    script = Script('Script de teste', soma, a=1, b=2)
    script.set_code_start(soma_start, a=2, b=2)
    script.run(False)
  except Exception as e:
    assert str(e) == 'test'


# Teste de execução
def test_model_script_singleton():
  script = Script('Script de teste', None)
  assert script is Script('Script de teste', None), "Singleton"
