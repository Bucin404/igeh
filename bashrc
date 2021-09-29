cd igeh
clear
echo "(1) Buat akun instagram otomatis"
echo "(2) Hack akun instagram"
echo -n "Nomor : "
read VAR

if [[ $VAR -gt 1 ]]
then
  python create.py
else
  python igeh.py
fi
   
