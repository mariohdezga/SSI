#Autor: Mario Hernandez Garcia
#Email: alu0101346908@ull.edu.es
#Práctica 4: Generador C/A de GPS mod polinomio realimentacion LSFR1 por id de satelite

#Costantes de colores para la salida por pantalla
RED = "\033[2;31;40m"
CYAN = "\033[2;36;40m"
GREEN = "\033[2;32;40m"
CLEAR_COLOR = "\033[0;0m"

#Funcion que recibe la string de entrada por consola y la transforma a una string binaria, en caso de que la funcion de 
# conversion no cubra los 8bits que definen un valor en la tabla ascii rellenamos con ceros ya que estos se omiten en la conversion
def str_to_ascii_to_bin(input_string):
    result = ""
    for i in range(len(input_string)):
        bin_result = bin(ord(input_string[i]))[2:]
        if (len(bin_result) == 8):
            result += bin_result
        else:
            while len(bin_result) < 8 :
                bin_result = '0' + bin_result
            result += bin_result
    return result

#Funcion que realiza la operacion xor entre dos strings binarias, para ello se recorre la string binaria valor a valor, 
# se transforma en entero, se realiza la operacion xor y este se vuelve a transformar en string que se añadira a una vacia que retornaremos
def xor_strings(s,t):
    return "".join(str(int(a,2) ^ int(b,2)) for a,b in zip(s,t))

#Funcion que recibe una string binaria y la pasa a ASCII, para ello se recorre la string binaria de 8 en 8 posiciones, 
# se pasa a entero y se utiliza char sobre ese entero para realizar la conversion, esto se añade en cada iteracion a una string nueva
def bin_to_ascii_to_str(input_string):
    return "".join([chr(int(input_string[i:i+8],2)) for i in range(0,len(input_string),8)])

#Recibe el vector del generador, los polinomios de realimentacion y los de salida, en la funcion se desplaza el vector a la derecha, se hacen las operaciones xor entre los valores que definen los polinomios
#y se añade al principio del vector el resultado de el xor de realimentacion, se devuelve el resultado de las xor del polinomio de salida
def rightShift(inputLFSR, re_polinomy, out_polinomy):
  dummy_vector = [0] + (inputLFSR[0:len(inputLFSR)-1])
  for i in range(len(re_polinomy)):
    if i == 0 :
      xor_result1 = inputLFSR[re_polinomy[i]-1]
    else:
      xor_result1 = xor_result1 ^ inputLFSR[re_polinomy[i]-1]
    
  for i in range(len(out_polinomy)):
    if i == 0 :
      xor_result2 = inputLFSR[out_polinomy[i]-1]
    else:
      xor_result2 = xor_result2 ^ inputLFSR[out_polinomy[i]-1]
  dummy_vector[0] = xor_result1
  print(f"Realimentacion: {xor_result1}")
  return [dummy_vector,xor_result2];

#Algoritmo gps C/A, recibe los vectores de los LSFR inicializados a 1, los polinomios de ambos tanto de salida como de entrada y el numero de iteraciones a realizar
#Devuelve todos los bits cifrantes de resultantes de las iteraciones
def gpsCA(result_vector_1, result_vector_2, polinomy_out_1, polinomy_out_2, polinomy_re_1, polinomy_re_2, cypher_length):
  out_1 = 0
  out_2 = 0
  dummy = ""
  for i in range(int(cypher_length)):
    print("\nLSFR1: ")
    print(result_vector_1)
    [result_vector_1,out_1] = rightShift(result_vector_1, polinomy_re_1, polinomy_out_1)
    print("\nLSFR2: ")
    print(result_vector_2)
    [result_vector_2,out_2] = rightShift(result_vector_2, polinomy_re_2, polinomy_out_2)
    print(f"\nBit cifrante {i+1} :" + str((out_1^out_2)))
    dummy += str((out_1^out_2))
  return dummy
#Diccionario que se utiliza para obtener los Taps segun el id del satelite que queramos
def idDictionary(id_sat):
  if (id_sat == 1):
    return [2,6]
  if (id_sat == 2):
    return [3,7]
  if (id_sat == 3):
    return [4,8]
  if (id_sat == 4):
    return [5,9]
  if (id_sat == 5):
    return [1,9]
  if (id_sat == 6):
    return [2,10]
  if (id_sat == 7):
    return [1,8]
  if (id_sat == 8):
    return [2,9]
  if (id_sat == 9):
    return [3,10]
  if (id_sat == 10):
    return [2,3]
  if (id_sat == 11):
    return [3,4]
  if (id_sat == 12):
    return [5,6]
  if (id_sat == 13):
    return [6,7]
  if (id_sat == 14):
    return [7,8]
  if (id_sat == 15):
    return [8,9]
  if (id_sat == 16):
    return [9,10]
  if (id_sat == 17):
    return [1,4]
  if (id_sat == 18):
    return [2,5]
  if (id_sat == 19):
    return [3,6]
  if (id_sat == 20):
    return [4,7]
  if (id_sat == 21):
    return [5,8]
  if (id_sat == 22):
    return [6,9]
  if (id_sat == 23):
    return [1,3]
  if (id_sat == 24):
    return [4,6]
  if (id_sat == 25):
    return [5,7]
  if (id_sat == 26):
    return [6,8]
  if (id_sat == 27):
    return [7,9]
  if (id_sat == 28):
    return [8,10]
  if (id_sat == 29):
    return [1,6]
  if (id_sat == 30):
    return [2,7]
  if (id_sat == 31):
    return [3,8]
  if (id_sat == 32):
    return [4,9]

polinomy_re_1 = [3,10]
polinomy_out_1 = [10]
result_vector_1 = [1,1,1,1,1,1,1,1,1,1]
polinomy_re_2 = [2,3,6,8,9,10]
print("Introduzca el mensaje a encriptar:")
message = input()
cypher_length = len(message)*8
print("Introduzca el id del satelite para LSFR1 (1-32):")
id_sat_1 = input()
print("Introduzca el id del satelite para LSFR2 (1-32):")
id_sat_2 = input()
#print("Introduzca la longitud de la secuencia de salida:")
#cypher_length = input()
polinomy_re_1 = idDictionary(int(id_sat_1))
polinomy_out_2 = idDictionary(int(id_sat_2))
result_vector_2 = [1,1,1,1,1,1,1,1,1,1]
dummy = gpsCA(result_vector_1, result_vector_2, polinomy_out_1, polinomy_out_2, polinomy_re_1, polinomy_re_2, cypher_length)
print(f"Mensaje en binario: \n {str_to_ascii_to_bin(message)} ")
print(f"Secuencia C/A PRN1 de longitud {str(cypher_length)} : {dummy}")
encrypted_message_bin = xor_strings(dummy,str_to_ascii_to_bin(message))
encrypted_message_ascii = bin_to_ascii_to_str(encrypted_message_bin)
print(f"Mensaje encriptado binario: \n {encrypted_message_bin} ")
print(f"Mensaje encriptado ascii: \n {encrypted_message_ascii} ")

dummy = gpsCA(result_vector_1, result_vector_2, polinomy_out_1, polinomy_out_2, polinomy_re_1, polinomy_re_2, cypher_length)

print(f"Secuencia descifrante C/A PRN1 de longitud {str(cypher_length)} : {dummy}")
decrypted_message_bin = xor_strings(encrypted_message_bin,dummy)
decrypted_message_ascii = bin_to_ascii_to_str(decrypted_message_bin)
print(f"Mensaje desencriptado binario: \n {decrypted_message_bin} ")
print(f"Mensaje desencriptado ascii: \n {decrypted_message_ascii} ")