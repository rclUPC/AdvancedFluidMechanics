/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Description
    Template for use with codeStream.

\*---------------------------------------------------------------------------*/

#include "dictionary.H"
#include "fieldTypes.H"
#include "Ostream.H"
#include "Pstream.H"
#include "read.H"
#include "unitConversion.H"

//{{{ begin codeInclude

//}}} end codeInclude

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    void codeStream_ded01f6f5f74c6edd68ffe5b75850d1f6c11e24e
    (
        Ostream& os,
        const dictionary& dict
    )
    {
//{{{ begin code
        #line 137 "/home/robert/GDriveUPC/Documents/asignaturas/AdvancedFluidMechanics/JupyterNotebooks/3-Turbulence/OF11/rotor2D/system/blockMeshDict/#codeStream"
const label viN = 4*dict.lookupScoped<label>("nBlades", true, false);

            auto makeArc = [&](const label v0, const label v1)
            {
                for (label i = 0; i < 2; ++ i)
                {
                    os  << "arc " << v0%viN + i*viN << ' ' << v1%viN + i*viN << ' '
                        << 360/scalar(dict.lookupScoped<label>("nBlades", true, false)) << ' ' << vector(0, 0, 1) << nl;
                }
            };

            for (label i = 0; i < dict.lookupScoped<label>("nBlades", true, false); i ++)
            {
                const label vi0 = i*4;
                makeArc(vi0+1, vi0+4);
                makeArc(vi0+2, vi0+6);
                makeArc(vi0+3, vi0+7);
            }
//}}} end code
    }
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

